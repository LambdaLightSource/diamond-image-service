import asyncio
import os
from datetime import datetime

import aioboto3
import pytz
from botocore.config import Config


class StorageManager:
    def __init__(self):
        self.session = aioboto3.Session()
        self.bucket_name = os.environ.get("BUCKET_NAME")

    async def list_and_delete_old_objects(self):
        print("Listing objects...")
        async with self.session.client(
            "s3",
            endpoint_url=os.environ.get("EP_URL"),
            aws_access_key_id=os.environ.get("KEY_ID"),
            aws_secret_access_key=os.environ.get("ACCESS_KEY"),
            config=Config(signature_version="s3v4"),
        ) as s3_client:
            paginator = s3_client.get_paginator("list_objects_v2")
            async for page in paginator.paginate(Bucket=self.bucket_name):
                if "Contents" in page:
                    for obj in page["Contents"]:
                        print(f"Checking object: {obj['Key']}")
                        await self.check_and_delete_object(s3_client, obj["Key"])

    async def check_and_delete_object(self, s3_client, key):
        expiration_date = await self.fetch_expiration_date(s3_client, key)
        if expiration_date:
            current_time_uk = datetime.now(pytz.timezone("Europe/London"))
            if current_time_uk >= expiration_date:
                await self.delete_object(s3_client, key)

    async def fetch_expiration_date(self, s3_client, key):
        print(f"Fetching object for metadata: {key}")
        response = await s3_client.get_object(Bucket=self.bucket_name, Key=key)
        async with response["Body"]:
            print(f"Got object: {key}")
            expiration_date_str = response["Metadata"].get("expiration_date")
            if expiration_date_str:
                expiration_date = datetime.strptime(
                    expiration_date_str, "%Y-%m-%dT%H:%M:%SZ"
                )
                expiration_date = pytz.timezone("Europe/London").localize(
                    expiration_date
                )
                return expiration_date
            else:
                print(f"No upload_time metadata found for {key}")

    async def delete_object(self, s3_client, key):
        print(f"Attempting to delete {key}")
        delete_response = await s3_client.delete_object(
            Bucket=self.bucket_name, Key=key
        )
        if delete_response["ResponseMetadata"]["HTTPStatusCode"] == 204:
            print(f"Delete response for {key}: {delete_response}")
        else:
            print(f"Failed to delete {key}")


async def main():
    storage_manager = StorageManager()
    await storage_manager.list_and_delete_old_objects()


if __name__ == "__main__":
    asyncio.run(main())
