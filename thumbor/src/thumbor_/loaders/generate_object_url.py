import os
import urllib.parse

import aioboto3
from botocore.config import Config


async def generate_encoded_url(input_key):
    session = aioboto3.Session()
    async with session.client(
        "s3",
        endpoint_url=os.environ.get("EP_URL"),
        aws_access_key_id=os.environ.get("KEY_ID"),
        aws_secret_access_key=os.environ.get("ACCESS_KEY"),
        region_name="eu-west-2",
        config=Config(signature_version="s3v4"),
    ) as client:
        response = await client.generate_presigned_url(
            "get_object",
            ExpiresIn=3600,
            Params={"Bucket": os.environ.get("BUCKET_NAME"), "Key": input_key},
        )
        encoded_url = urllib.parse.quote(response)
        return encoded_url
