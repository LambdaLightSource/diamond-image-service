import loaders.bucket_details as bucket_details
import boto3
from botocore.client import Config
import urllib.parse

s3_buckets = boto3.resource(
        service_name="s3",
        endpoint_url=bucket_details.ep_url,
        aws_access_key_id=bucket_details.key_id,
        aws_secret_access_key=bucket_details.access_key,
        config=Config(signature_version="s3v4"),
        )

my_bucket = s3_buckets.Bucket(bucket_details.bucket_name)
client = s3_buckets.meta.client

def generate_encoded_url(input_key):
    generated_url = client.generate_presigned_url("get_object", ExpiresIn=3600, Params={"Bucket":bucket_details.bucket_name, "Key":input_key})
    encoded_url = urllib.parse.quote(generated_url)
    return encoded_url