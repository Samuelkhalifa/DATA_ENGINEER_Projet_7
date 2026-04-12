def get_loaded_files_from_snowflake():

    import os
    import snowflake.connector
    from dotenv import load_dotenv
   
    load_dotenv()

    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
    SNOWFLAKE_DB = os.getenv("SNOWFLAKE_DB")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

    conn = snowflake.connector.connect(
            user = SNOWFLAKE_USER,
            password = SNOWFLAKE_PASSWORD,
            account = SNOWFLAKE_ACCOUNT,
            warehouse = SNOWFLAKE_WAREHOUSE,
            database = SNOWFLAKE_DB,
            schema = SNOWFLAKE_SCHEMA
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT filename
        FROM bronze_stock_quotes_raw
    """)

    loaded_files = cursor.fetchall()

    loaded_files_from_sf = []

    for loaded_file in loaded_files:
        loaded_files_from_sf.append(loaded_file[0])

    print(loaded_files_from_sf)


    return loaded_files_from_sf








