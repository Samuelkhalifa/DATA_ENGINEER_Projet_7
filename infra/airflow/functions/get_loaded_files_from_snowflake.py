def get_loaded_files_from_snowflake():

    import os
    import snowflake.connector
    from dotenv import load_dotenv
   

    # connection to .env
    load_dotenv()


    # snowflake connection variables
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
    SNOWFLAKE_DB = os.getenv("SNOWFLAKE_DB")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")


    # settings for connection to snowflake database
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


    # SQL writing to query snowflake database and see all already-loaded files
    cursor.execute("""
        SELECT filename
        FROM bronze_stock_quotes_raw
    """)


    # new variables
    loaded_files = cursor.fetchall()
    loaded_files_from_sf = []


    # loop to fill "loaded_files_from_sf"
    for loaded_file in loaded_files:
        loaded_files_from_sf.append(loaded_file[0])

    
    # closing SQL writing necessary lines
    cursor.close()
    conn.close()


    return loaded_files_from_sf








