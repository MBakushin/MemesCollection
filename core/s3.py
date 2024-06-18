import boto3
from botocore.client import Config
from .config import settings


s3_client = boto3.client(
    's3',
    endpoint_url=settings.S3_ENDPOINT_URL,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    config=Config(signature_version='s3v4')
)


def upload_file_to_s3(file, bucket_name, object_name):
    try:
        s3_client.upload_fileobj(file, bucket_name, object_name)
        return f"{settings.S3_ENDPOINT_URL}/{bucket_name}/{object_name}"
    except Exception as e:
        print(e)
        return None
