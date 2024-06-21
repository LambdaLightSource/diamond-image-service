import aioboto3
from thumbor.storages import BaseStorage
import loaders.bucket_details as bucket_details
from botocore.client import Config
from botocore.exceptions import ClientError

class Storage(BaseStorage):
    def __init__(self, context):
        super(Storage, self).__init__(context)
        self.s3_client = boto3.client(
            's3',
            endpoint_url=bucket_details.ep_url,
            aws_access_key_id=bucket_details.key_id,
            aws_secret_access_key=bucket_details.access_key,
            config=Config(signature_version="s3v4")
        )
        self.bucket_name = bucket_details.bucket_name

    def put(self, path, file_bytes):
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=path, Body=file_bytes)
            return path
        except ClientError as e:
            raise Exception(f"Failed to upload {path}: {str(e)}")

    def delete(self, path):
        try:
            response = self.s3_client.delete_object(Bucket=self.bucket_name, Key=path)
            if response['ResponseMetadata']['HTTPStatusCode'] == 204:
                return path
            else:
                raise Exception(f"Failed to delete {path}")
        except ClientError as e:
            raise Exception(f"Failed to delete {path}: {str(e)}")
        
    def exists(self, path):
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=path)
            return response['Body'].read()
        except self.s3_client.exceptions.NoSuchKey:
            return None


