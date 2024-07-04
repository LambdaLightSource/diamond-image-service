import urllib.parse

import aioboto3
import loaders.bucket_details as bucket_details
from botocore.config import Config


async def generate_encoded_url(input_key):
    session = aioboto3.Session()
    async with session.client(
        "s3",
        endpoint_url=bucket_details.ep_url,
        aws_access_key_id=bucket_details.key_id,
        aws_secret_access_key=bucket_details.access_key,
        region_name="eu-west-2",
        config=Config(signature_version="s3v4"),
    ) as client:
        response = await client.generate_presigned_url(
            "get_object",
            ExpiresIn=3600,
            Params={"Bucket": bucket_details.bucket_name, "Key": input_key},
        )
        encoded_url = urllib.parse.quote(response)
        return encoded_url
