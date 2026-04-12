def load_into_snowflake(**kwargs):
    
    import os
    import snowflake.connector
    import boto3
    from dotenv import load_dotenv
   
    load_dotenv()

    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
    SNOWFLAKE_DB = os.getenv("SNOWFLAKE_DB")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
    BUCKET = os.getenv("BUCKET")

    loaded_files_from_sf = kwargs['ti'].xcom_pull(task_ids='get_loaded_files_from_snowflake')
    loaded_files_from_sf_well_named = [f.split("/")[-1].replace(".json.gz", "") for f in loaded_files_from_sf]
    
    files = kwargs['ti'].xcom_pull(task_ids='download_from_minio')
    files_well_named = [f.split("/")[-1].replace(".json", "") for f in files]

    #files_raw = files

    def normalize(f):
        return f.split("/")[-1].replace(".json", "")


    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY
    )
    conn = snowflake.connector.connect(
        user = SNOWFLAKE_USER,
        password = SNOWFLAKE_PASSWORD,
        account = SNOWFLAKE_ACCOUNT,
        warehouse = SNOWFLAKE_WAREHOUSE,
        database = SNOWFLAKE_DB,
        schema = SNOWFLAKE_SCHEMA
    )

    cursor = conn.cursor()

    downloaded_files_to_ingest =[]

    TMP_DIR_PATH = f"/tmp/minio_downloads/"
    os.makedirs(TMP_DIR_PATH, exist_ok=True)   

    for file in [f for f in files if normalize(f) not in loaded_files_from_sf_well_named]:
        ABS_FILE_PATH = os.path.abspath(os.path.join(TMP_DIR_PATH, os.path.basename(file)))
        s3.download_file(BUCKET, file, ABS_FILE_PATH)
        downloaded_files_to_ingest.append(ABS_FILE_PATH)
        
    for df in downloaded_files_to_ingest:
        cursor.execute(f"""
            PUT file://{df} @%bronze_stock_quotes_raw
        """)
        os.remove(df)
        print(f"{df} successfully put into stage")

    cursor.execute(f"""
        COPY INTO bronze_stock_quotes_raw (raw, filename)
        FROM (
            SELECT
                $1,
                METADATA$FILENAME
            FROM @%bronze_stock_quotes_raw
        )
        FILE_FORMAT = (TYPE=JSON)
    """)

    cursor.execute(f"""
        REMOVE @%bronze_stock_quotes_raw;
    """)

    cursor.close()
    conn.close()
