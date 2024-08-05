import os
from io import BytesIO

import tornado.web

from thumbor_.s3_store.s3_storage import Storage


class UploadHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.bucket_name = os.environ.get("BUCKET_NAME")
        self.storage = Storage(context=self)

    async def put(self):
        fileinfo = self.request.files["media"][0]
        filename = fileinfo["filename"]
        filebody = fileinfo["body"]
        lifespan = self.get_query_argument("lifespan", default="180")
        try:
            path = await self.storage.put(filename, BytesIO(filebody), lifespan)
            self.write(
                {
                    "status": "success",
                    "message": f"File {path} uploaded successfully to S3",
                }
            )
        except Exception as e:
            self.write({"status": "error", "message": str(e)})

    async def delete(self):
        filename = self.get_argument("filename")
        try:
            path = await self.storage.delete(filename)
            self.write(
                {
                    "status": "success",
                    "message": f"File {path} deleted successfully from S3",
                }
            )
        except Exception as e:
            self.write({"status": "error", "message": str(e)})
