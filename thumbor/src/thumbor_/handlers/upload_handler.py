from s3_store.s3_storage import Storage
from io import BytesIO
import tornado.web

class UploadHandler(tornado.web.RequestHandler):
    def initialize(self, bucket_name):
        self.bucket_name = bucket_name
        self.storage = Storage(context=self)

    async def put(self):
        fileinfo = self.request.files['media'][0]
        filename = fileinfo['filename']
        filebody = fileinfo['body']
        try:
            path = await self.storage.put(filename, BytesIO(filebody))
            self.write({'status': 'success', 'message': f'File {path} uploaded successfully to S3'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})


    async def delete(self):
        filename = self.get_argument('filename')
        try:
            path = await self.storage.delete(filename)
            self.write({'status': 'success', 'message': f'File {path} deleted successfully from S3'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})