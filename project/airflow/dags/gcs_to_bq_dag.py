import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'github_data_all')

DATASET = "github_all"
INPUT_PART = "raw"
INPUT_FILETYPE = "parquet"

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="gcs_to_bq_dag",
    schedule_interval="55 * * * *",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:


    move_files_gcs_task = GCSToGCSOperator(
        task_id=f'move_{DATASET}_files_task',
        source_bucket=BUCKET,
        source_object=f'{INPUT_PART}/*.{INPUT_FILETYPE}',
        destination_bucket=BUCKET,
        destination_object=f'github/{DATASET}',
        move_object=True
    )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id=f"bq_{DATASET}_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": f"{DATASET}_external_table",
            },
            "externalDataConfiguration": {
                "autodetect": "True",
                "sourceFormat": f"{INPUT_FILETYPE.upper()}",
                "sourceUris": [f"gs://{BUCKET}/github/*"],
            },
        },
    )

    CREATE_BQ_TBL_QUERY = (
        f"CREATE OR REPLACE TABLE {BIGQUERY_DATASET}.{DATASET} \
        AS \
        SELECT * FROM {BIGQUERY_DATASET}.{DATASET}_external_table;"
    )

    # Create a partitioned table from external table
    bq_create_partitioned_table_job = BigQueryInsertJobOperator(
        task_id=f"bq_create_{DATASET}_table_task",
        configuration={
            "query": {
                "query": CREATE_BQ_TBL_QUERY,
                "useLegacySql": False,
            }
        }
    )

    move_files_gcs_task >> bigquery_external_table_task >> bq_create_partitioned_table_job
