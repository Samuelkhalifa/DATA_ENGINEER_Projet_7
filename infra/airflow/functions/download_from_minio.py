def download_from_minio():

    import os
    import boto3
    from dotenv import load_dotenv

    load_dotenv()

    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    BUCKET = os.getenv("BUCKET")

    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY
    )

    paginator = s3.get_paginator("list_objects_v2")
    files = []

    for page in paginator.paginate(Bucket=BUCKET):
        for obj in page.get("Contents", []):
            files.append(obj["Key"])

    return files

