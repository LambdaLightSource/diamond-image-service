import argparse
import asyncio
from datetime import datetime, timedelta

import aioboto3
import pytz
from botocore.config import Config
from botocore.exceptions import ClientError
from loaders import bucket_details as bucket_details


class StorageManager:
    def __init__(self, expiry_days):
        self.session = aioboto3.Session()
        self.bucket_name = bucket_details.bucket_name
        self.expiry_duration = timedelta(days=expiry_days)

    async def list_and_delete_old_objects(self):
        print("Listing objects...")
        async with self.session.client(
            "s3",
            endpoint_url=bucket_details.ep_url,
            aws_access_key_id=bucket_details.key_id,
            aws_secret_access_key=bucket_details.access_key,
            config=Config(signature_version="s3v4"),
        ) as s3_client:
            paginator = s3_client.get_paginator("list_objects_v2")
            async for page in paginator.paginate(Bucket=self.bucket_name):
                if "Contents" in page:
                    for obj in page["Contents"]:
                        print(f"Checking object: {obj['Key']}")
                        await self.check_and_delete_object(s3_client, obj["Key"])

    async def check_and_delete_object(self, s3_client, key, timeout=100):
        print(f"Fetching object: {key}")
        try:
            response = await asyncio.wait_for(
                s3_client.get_object(Bucket=self.bucket_name, Key=key), timeout
            )
            async with response["Body"]:
                print(f"Got object: {key}")
                upload_time_str = response["Metadata"].get("upload_time")

                if upload_time_str:
                    uk_zone = pytz.timezone("Europe/London")
                    upload_time = datetime.strptime(
                        upload_time_str, "%Y-%m-%dT%H:%M:%SZ"
                    )
                    upload_time = uk_zone.localize(upload_time)
                    current_time_uk = datetime.now(uk_zone)
                    time_diff = current_time_uk - upload_time

                    print(f"Time difference for {key}: {time_diff}")
                    if time_diff > self.expiry_duration:
                        print(f"Attempting to delete {key}")
                        delete_response = await s3_client.delete_object(
                            Bucket=self.bucket_name, Key=key
                        )
                        print(f"Delete response for {key}: {delete_response}")
                else:
                    print(f"No upload_time metadata found for {key}")
        except asyncio.TimeoutError:
            print(f"Timeout occurred while fetching object: {key}")
        except ClientError as e:
            print(f"Failed to fetch or delete {key} due to a client error: {str(e)}")
        except Exception as e:
            print(f"Unexpected exception {key}: {str(e)}")


async def main():
    parser = argparse.ArgumentParser(
        description="Manage S3 bucket storage based on object age."
    )
    parser.add_argument(
        "-d",
        "--days",
        type=int,
        default=180,
        help="Number of days after which to delete old objects (default is 180 days).",
    )
    args = parser.parse_args()

    storage_manager = StorageManager(expiry_days=args.days)
    await storage_manager.list_and_delete_old_objects()


if __name__ == "__main__":
    asyncio.run(main())
