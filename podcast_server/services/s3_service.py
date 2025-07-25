import os
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

def upload_file(file_path, key):
    s3_client.upload_file(file_path, S3_BUCKET_NAME, key)
    return f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{key}"

# def download_file(key, download_path):
#     s3_client.download_file(S3_BUCKET_NAME, key, download_path)

def upload_folder(folder_path, s3_prefix=""):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, folder_path)
            s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")
            s3_client.upload_file(local_path, S3_BUCKET_NAME, s3_key)
            
def download_folder(s3_prefix, local_folder):
    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=S3_BUCKET_NAME, Prefix=s3_prefix):
        for obj in page.get('Contents', []):
            s3_key = obj['Key']
            rel_path = os.path.relpath(s3_key, s3_prefix)
            local_path = os.path.join(local_folder, rel_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            s3_client.download_file(S3_BUCKET_NAME, s3_key, local_path)

def get_presigned_url(key, expires_in=36000):
    return s3_client.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET_NAME, 'Key': key},
        ExpiresIn=expires_in
    )