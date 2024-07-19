import asyncio
from datetime import datetime, timedelta

import aioboto3
import pytz
from loaders import bucket_details

config = {
    "endpoint_url": bucket_details.ep_url,
    "aws_access_key_id": bucket_details.key_id,
    "aws_secret_access_key": bucket_details.access_key,
    "region_name": "eu-west-2",
}

uk_zone = pytz.timezone("Europe/London")

days_ago = [1, 30, 180, 365, 1095]


async def upload_file(s3_client, bucket_name, key, days_old):
    date_uploaded = datetime.now(uk_zone) - timedelta(days=days_old)
    metadata = {"upload_time": date_uploaded.strftime("%Y-%m-%dT%H:%M:%SZ")}
    await s3_client.put_object(
        Bucket=bucket_name, Key=key, Body=b"Sample file content", Metadata=metadata
    )
    print(f"Uploaded {key} with upload_time: {metadata['upload_time']}")


async def populate_bucket():
    session = aioboto3.Session()
    async with session.client("s3", **config) as s3_client:
        for days in days_ago:
            key = f"testfile_{days}_days_old.txt"
            await upload_file(s3_client, bucket_details.bucket_name, key, days)


async def main():
    await populate_bucket()


if __name__ == "__main__":
    asyncio.run(main())
