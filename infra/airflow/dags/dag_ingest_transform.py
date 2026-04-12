from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from functions.download_from_minio import download_from_minio
from functions.load_into_snowflake import load_into_snowflake


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}



with DAG(
    "ingest_transform",
    default_args=default_args,
    schedule=None,
    catchup=False
) as dag:
    
    task1 = PythonOperator(
        task_id="download_from_minio",
        python_callable=download_from_minio
    )
    task2 = PythonOperator(
        task_id="load_into_snowflake",
        python_callable=load_into_snowflake
    )
    task3 = BashOperator(
        task_id="dbt_transformations",
        bash_command="cd /opt/airflow/dbt && dbt run --profiles-dir .dbt_profiles/"
    )

    task1 >> task2 >> task3