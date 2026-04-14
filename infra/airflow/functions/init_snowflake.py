def init_snowflake():

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
        CREATE DATABASE IF NOT EXISTS stock_quotes_db
    """)

    cursor.execute("""
        USE stock_quotes_db;
    """)

    cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS stock_quotes_db.common;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_quotes_db.common.bronze_stock_quotes_raw(
            raw VARIANT,
            loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
            filename STRING
        );
    """)

    # closing SQL writing necessary lines
    conn.commit()
    cursor.close()
    conn.close()