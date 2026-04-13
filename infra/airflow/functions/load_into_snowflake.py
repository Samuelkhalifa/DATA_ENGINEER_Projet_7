def load_into_snowflake(**kwargs):
    
    import os
    import snowflake.connector
    import boto3
    from dotenv import load_dotenv
   

    # connection to .env
    load_dotenv()


    # snowflake and minIO connection variables
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


    # retrieval of returns from previous dag's functions (airflow's xcom : cross-communication)
    loaded_files_from_sf = kwargs['ti'].xcom_pull(task_ids='get_loaded_files_from_snowflake')
    files = kwargs['ti'].xcom_pull(task_ids='download_from_minio')


    # renaming 
    loaded_files_from_sf_well_named = [f.split("/")[-1].replace(".json.gz", "") for f in loaded_files_from_sf]
    

    # renaming def for "files" (to be used later)
    def normalize(f):
        return f.split("/")[-1].replace(".json", "")


    # settings for connection to minio s3 and snowflake database
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


    # variable for SQL writing
    cursor = conn.cursor()



    downloaded_files_to_ingest =[]


    # creating tmp path to temporarily store downloaded files from minIO
    TMP_DIR_PATH = f"/tmp/minio_downloads/"
    os.makedirs(TMP_DIR_PATH, exist_ok=True)   


    # loop to select files not already loaded in snowflake database to avoid duplicates
    for file in [f for f in files if normalize(f) not in loaded_files_from_sf_well_named]:
        # construct absolute path for futurs selected files
        ABS_FILE_PATH = os.path.abspath(os.path.join(TMP_DIR_PATH, os.path.basename(file)))
        # downloading and stocking selected files
        s3.download_file(BUCKET, file, ABS_FILE_PATH)
        downloaded_files_to_ingest.append(ABS_FILE_PATH)
        

    # loop to send each selected file into snowflake table's stage (@%) then remove it from tmp os directory
    for df in downloaded_files_to_ingest:
        cursor.execute(f"""
            PUT file://{df} @%bronze_stock_quotes_raw
        """)
        os.remove(df)
        print(f"{df} successfully put into stage")


    # SQL writing to send data from stage to table (in snowflake)
    cursor.execute(f"""
        COPY INTO bronze_stock_quotes_raw (raw, filename)
        FROM (
            SELECT
                $1,
                METADATA$FILENAME
            FROM @%bronze_stock_quotes_raw
        )
        FILE_FORMAT = (TYPE=JSON)
    """) # => $1 load entire raw JSON file, METADATA$FILENAME loads original file name from table's stage


    # empty table's stage to avoid reloading all previous rows still within
    cursor.execute(f"""
        REMOVE @%bronze_stock_quotes_raw;
    """)


    # closing SQL writing necessary lines
    cursor.close()
    conn.close()
