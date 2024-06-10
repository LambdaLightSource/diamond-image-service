from s3_store.s3_storage import Storage
from io import BytesIO
import loaders.bucket_details as bucket_details
from botocore.config import Config as BotoConfig
import boto3
import tornado.web



class UploadHandler(tornado.web.RequestHandler):
    def initialize(self, bucket_name):
        self.bucket_name = bucket_name
        self.storage = Storage(context=self)
        self.s3 = boto3.client(
            's3',
            region_name="eu-west-2",
            endpoint_url=bucket_details.ep_url,
            aws_access_key_id=bucket_details.key_id,
            aws_secret_access_key=bucket_details.access_key,
            config=BotoConfig(signature_version="s3v4"),
        )

    def put(self):
        fileinfo = self.request.files['media'][0]
        filename = fileinfo['filename']
        filebody = fileinfo['body']
        try:
            path = self.storage.put(filename, BytesIO(filebody))
            self.write({'status': 'success', 'message': f'File {path} uploaded successfully to S3'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})


    def delete(self):
        filename = self.get_argument('filename')
        try:
            path = self.storage.delete(filename)
            self.write({'status': 'success', 'message': f'File {path} deleted successfully from S3'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})