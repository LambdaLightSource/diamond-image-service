import logging
import os
from io import BytesIO

import tornado.web

from thumbor_.s3_store.s3_storage import Storage

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class UploadHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.bucket_name = os.environ.get("BUCKET_NAME")

    async def put(self):
        fileinfo = self.request.files.get("media")
        if not fileinfo:
            self.set_status(400)
            self.write({"status": "error", "message": "No file uploaded"})
            return

        fileinfo = fileinfo[0]
        filename = fileinfo["filename"]
        filebody = fileinfo["body"]
        lifespan = self.get_query_argument("lifespan", default="180")

        try:
            async with Storage(context=self) as storage:
                path = await storage.put(filename, BytesIO(filebody), lifespan)
            self.set_status(201)
            self.write(
                {
                    "status": "success",
                    "message": f"File {path} uploaded successfully to S3",
                }
            )
        except KeyError as e:
            logging.error(f"Key error: {e}")
            self.set_status(400)
            self.write({"status": "error", "message": f"Invalid data: {str(e)}"})
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            self.set_status(500)
            self.write({"status": "error", "message": "Internal server error"})

    async def delete(self):
        filename = self.get_argument("filename")
        try:
            async with Storage(context=self) as storage:
                path = await storage.delete(filename)
            self.set_status(200)
            self.write(
                {
                    "status": "success",
                    "message": f"File {path} deleted successfully from S3",
                }
            )
        except Exception as e:
            logging.error(f"Delete error: {e}")
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})
