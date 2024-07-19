from datetime import datetime, timedelta

import aioboto3
import loaders.bucket_details as bucket_details
import pytz
from botocore.config import Config
from botocore.exceptions import ClientError
from thumbor.storages import BaseStorage


class Storage(BaseStorage):
    def __init__(self, context):
        super().__init__(context)
        self.session = aioboto3.Session()
        self.bucket_name = bucket_details.bucket_name

    async def put(self, path, file_bytes, lifespan):
        uk_zone = pytz.timezone("Europe/London")
        current_time = datetime.now(uk_zone)
        expiration_date = current_time + timedelta(days=int(lifespan))

        metadata = {
            "upload_time": current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "expiration_date": expiration_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        async with self.session.client(
            "s3",
            endpoint_url=bucket_details.ep_url,
            aws_access_key_id=bucket_details.key_id,
            aws_secret_access_key=bucket_details.access_key,
            config=Config(signature_version="s3v4"),
        ) as s3_client:
            try:
                await s3_client.put_object(
                    Bucket=self.bucket_name,
                    Key=path,
                    Body=file_bytes,
                    Metadata=metadata,
                )
                return path
            except ClientError as e:
                raise Exception(f"Failed to upload {path}: {str(e)}") from e

    async def delete(self, path):
        async with self.session.client(
            "s3",
            endpoint_url=bucket_details.ep_url,
            aws_access_key_id=bucket_details.key_id,
            aws_secret_access_key=bucket_details.access_key,
            config=Config(signature_version="s3v4"),
        ) as s3_client:
            try:
                response = await s3_client.delete_object(
                    Bucket=self.bucket_name, Key=path
                )
                if response["ResponseMetadata"]["HTTPStatusCode"] == 204:
                    return path
                else:
                    raise Exception(f"Failed to delete {path}")
            except ClientError as e:
                raise Exception(f"Failed to delete {path}: {str(e)}") from e

    def exists(self, path):
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=path)
            return response["Body"].read()
        except self.s3_client.exceptions.NoSuchKey:
            return None
