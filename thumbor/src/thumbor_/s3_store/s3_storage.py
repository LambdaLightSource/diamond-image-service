import os
from datetime import datetime, timedelta

import aioboto3
import pytz
from botocore.config import Config
from botocore.exceptions import ClientError
from thumbor.storages import BaseStorage


class Storage(BaseStorage):
    def __init__(self, context):
        super().__init__(context)
        self.bucket_name = os.environ.get("BUCKET_NAME")

    async def __aenter__(self):
        self.session = aioboto3.Session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def put(self, path, file_bytes, lifespan):
        client_config = Config(
            signature_version="s3v4",
            max_pool_connections=32000,
            connect_timeout=1,
            read_timeout=1,
            retries={"max_attempts": 100000000, "mode": "adaptive"},
        )
        async with self.session.client(
            "s3",
            endpoint_url=os.environ.get("EP_URL"),
            aws_access_key_id=os.environ.get("KEY_ID"),
            aws_secret_access_key=os.environ.get("ACCESS_KEY"),
            config=client_config,
        ) as s3_client:
            uk_zone = pytz.timezone("Europe/London")
            current_time = datetime.now(uk_zone)
            expiration_date = current_time + timedelta(days=int(lifespan))

            metadata = {
                "upload_time": current_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "expiration_date": expiration_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

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
            # finally:
            #     await s3_client.close()

    async def delete(self, path):
        async with self.session.client(
            "s3",
            endpoint_url=os.environ.get("EP_URL"),
            aws_access_key_id=os.environ.get("KEY_ID"),
            aws_secret_access_key=os.environ.get("ACCESS_KEY"),
            config=Config(signature_version="s3v4"),
        ) as s3_client:
            try:
                response = await s3_client.delete_object(
                    Bucket=self.bucket_name, Key=path
                )
                if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 204:
                    return path
                else:
                    raise Exception(f"Failed to delete {path}")
            except ClientError as e:
                raise Exception(f"Failed to delete {path}: {str(e)}") from e
            # finally:
            #     await s3_client.close()

    async def exists(self, path):
        async with self.session.client(
            "s3",
            endpoint_url=os.environ.get("EP_URL"),
            aws_access_key_id=os.environ.get("KEY_ID"),
            aws_secret_access_key=os.environ.get("ACCESS_KEY"),
            config=Config(signature_version="s3v4"),
        ) as s3_client:
            try:
                await s3_client.get_object(Bucket=self.bucket_name, Key=path)
                return True
            except s3_client.exceptions.NoSuchKey:
                return False
            # finally:
            #     await s3_client.close()
