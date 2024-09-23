import asyncio
import os
from datetime import datetime, timedelta

import aioboto3
import pytz

config = {
    "endpoint_url": os.environ.get("EP_URL"),
    "aws_access_key_id": os.environ.get("KEY_ID"),
    "aws_secret_access_key": os.environ.get("ACCESS_KEY"),
    "region_name": "eu-west-2",
}

uk_zone = pytz.timezone("Europe/London")

lifespan_days = [1, 30, 180, 365, 1095]


async def upload_file(s3_client, bucket_name, key, lifespan):
    current_time = datetime.now(uk_zone)

    expiration_date = current_time - timedelta(days=lifespan)
    metadata = {
        "upload_time": current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "expiration_date": expiration_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    await s3_client.put_object(
        Bucket=bucket_name, Key=key, Body=b"Sample file content", Metadata=metadata
    )
    print(
        f"Uploaded {key} at upload_time: {metadata['upload_time']} "
        f"expiration_date: {metadata['expiration_date']}"
    )


async def populate_bucket():
    session = aioboto3.Session()
    async with session.client("s3", **config) as s3_client:
        for days in lifespan_days:
            key = f"testfile_{days}_days_expired.txt"
            await upload_file(s3_client, os.environ.get("BUCKET_NAME"), key, days)


async def main():
    await populate_bucket()


if __name__ == "__main__":
    asyncio.run(main())
