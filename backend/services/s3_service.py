import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import asyncio

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

def upload_folder(folder_path, s3_prefix=""):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, folder_path)
            s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")

            s3_client.upload_file(local_path, S3_BUCKET_NAME, s3_key)
            print(f"Uploaded file: {file}")
            
def download_folder(s3_prefix, local_folder):
    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=S3_BUCKET_NAME, Prefix=s3_prefix):
        for obj in page.get('Contents', []):
            s3_key = obj['Key']
            rel_path = os.path.relpath(s3_key, s3_prefix)
            local_path = os.path.join(local_folder, rel_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            s3_client.download_file(S3_BUCKET_NAME, s3_key, local_path)

def generate_signed_urls(prefix: str, expiration: int = 3600):
    """
    Generate signed URLs for all files under a given S3 prefix.

    Args:
        prefix (str): The folder (prefix) in S3.
        expiration (int): Expiration time for signed URL in seconds (default 1 hour).

    Returns:
        dict: { "file_key": "signed_url" }
    """
    signed_urls = {}

    try:
        # List all objects under the given prefix
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=prefix)

        if 'Contents' not in response:
            print(f"No files found in prefix: {prefix}")
            return signed_urls

        for obj in response['Contents']:
            key = obj['Key'].split("/")[-1]
            try:
                url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': S3_BUCKET_NAME, 'Key': key},
                    ExpiresIn=expiration
                )
                signed_urls[key] = url
            except ClientError as e:
                print(f"Failed to generate URL for {key}: {e}")

        return signed_urls
    except ClientError as e:
        print(f"[ERROR] Could not list objects for prefix {prefix}: {e}")
        return {}

def list_s3_files(prefix: str=""):
    """
    Lists all files in S3 under a given prefix.

    Args:
        prefix (str): The prefix (folder path) in the S3 bucket.

    Returns:
        list: A list of S3 keys (file paths) under the prefix.
    """
    files = []
    continuation_token = None

    try:
        while True:
            if continuation_token:
                response = s3_client.list_objects_v2(
                    Bucket=S3_BUCKET_NAME, Prefix=prefix, ContinuationToken=continuation_token
                )
            else:
                response = s3_client.list_objects_v2(
                    Bucket=S3_BUCKET_NAME, Prefix=prefix
                )

            for item in response.get("Contents", []):
                files.append(item["Key"])

            if response.get("IsTruncated"):  # More files to list
                continuation_token = response["NextContinuationToken"]
            else:
                break
    except Exception as e:
        print(f"[ERROR] Failed to list files from S3 prefix '{prefix}': {e}")
        return []

    return files
