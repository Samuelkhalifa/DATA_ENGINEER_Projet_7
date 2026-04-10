import os
import boto3
from dotenv import load_dotenv
import snowflake.connector



load_dotenv()



MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
BUCKET = os.getenv("BUCKET")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DB = os.getenv("SNOWFLAKE_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")



def load_to_snowflake():

    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:9002",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY
    )

    paginator = s3.get_paginator("list_objects_v2")
    files = []
    for page in paginator.paginate(Bucket=BUCKET):
        for obj in page.get("Contents", []):
            files.append(obj["Key"])
   
    conn = snowflake.connector.connect(
        user = SNOWFLAKE_USER,
        password = SNOWFLAKE_PASSWORD,
        account = SNOWFLAKE_ACCOUNT,
        warehouse = SNOWFLAKE_WAREHOUSE,
        database = SNOWFLAKE_DB,
        schema = SNOWFLAKE_SCHEMA
    )

    cursor = conn.cursor()

    downloaded_files =[]
    TMP_DIR_PATH = f"/tmp/minio_downloads/"
    os.makedirs(TMP_DIR_PATH, exist_ok=True)   

    for file in files:
        ABS_FILE_PATH = os.path.abspath(os.path.join(TMP_DIR_PATH, os.path.basename(file)))
        s3.download_file(BUCKET, file, ABS_FILE_PATH)
        downloaded_files.append(ABS_FILE_PATH)
        

    for df in downloaded_files:
        cursor.execute(f"""
            PUT file://{df} @%bronze_stock_quotes_raw
        """)
        os.remove(df)
        print(f"{df} successfully put into stage")

    cursor.execute(f"""
        COPY INTO bronze_stock_quotes_raw (raw)
        FROM @%bronze_stock_quotes_raw
        FILE_FORMAT = (TYPE=JSON)
    """)

    cursor.execute(f"""
        REMOVE @%bronze_stock_quotes_raw;
    """)

    cursor.close()
    conn.close()


load_to_snowflake()