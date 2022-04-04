from datetime import timedelta
import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import datetime
from airflow.utils.dates import timedelta

path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

with DAG(
    'dbt_dag',
    start_date=datetime(2021, 12, 23),
    description='An Airflow DAG to invoke simple dbt commands',
    schedule_interval=timedelta(days=1),
    depends_on_past= False,
) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f'cd {path_to_local_home}/github && dbt run --target prod'
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='dbt test'
    )

    dbt_run >> dbt_test