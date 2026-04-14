from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.models import DagRun
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
from functions.download_from_minio import download_from_minio
from functions.load_into_snowflake import load_into_snowflake
from functions.get_loaded_files_from_snowflake import get_loaded_files_from_snowflake
from functions.init_snowflake import init_snowflake



default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}



def check_first_run(**context):
    dag_id = context["dag_run"].dag_id
    dag_runs = DagRun.find(dag_id=dag_id)
    previous_runs = [run for run in dag_runs if run.execution_date < context["dag_run"].execution_date]
    if not previous_runs:
        return "first_run"
    else:
        return "not_first_run"



with DAG(
    "ingest_transform",
    default_args=default_args,
    schedule=None,
    catchup=False
) as dag:
    
    branch = BranchPythonOperator(
        task_id="check_first_dag_run",
        python_callable=check_first_run
    )
    task1_not_first_run = EmptyOperator(
        task_id="not_first_run"
    )
    task1_first_run = PythonOperator(
        task_id="first_run",
        python_callable=init_snowflake
    )
    task2 = PythonOperator(
        task_id="download_from_minio",
        python_callable=download_from_minio,
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS
    )
    task3 = PythonOperator(
        task_id="get_loaded_files_from_snowflake",
        python_callable=get_loaded_files_from_snowflake
    )
    task4 = PythonOperator(
        task_id="load_into_snowflake",
        python_callable=load_into_snowflake
    )
    task5 = BashOperator(
        task_id="dbt_transformations",
        bash_command="cd /opt/airflow/dbt && dbt run --profiles-dir .dbt_profiles/"
    )

    branch >> [task1_not_first_run, task1_first_run] >> task2 >> task3 >> task4 >> task5