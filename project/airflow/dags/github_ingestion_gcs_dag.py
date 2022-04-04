"""
This DAG is responsible for downloading github data compressing into parquet and uploading to GCS
Runs hourly for each hourly github file
"""
import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from pyarrow import json
import pyarrow.parquet as pq
from google.cloud import storage
from datetime import datetime
import pandas as pd

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
#https://data.gharchive.org/2015-01-01-15.json.gz
base_file_name = '{{ execution_date.strftime(\'%Y-%m-%d-%-H\') }}'
dataset_file = f'{base_file_name}.json.gz'
dataset_url = f"https://data.gharchive.org/{dataset_file}"
parquet_file = dataset_file.replace('.json.gz', '.parquet')
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'stg_github')


# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
}

def ungzip(src_file):
    if not src_file.endswith('.gz'):
        logging.error("Can only accept source files in GZ format, for the moment")
        return
    with gzip.open(src_file, 'r') as f_in , open(src_file[:-3], 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def format_to_parquet(src_file: str):
    if not src_file.endswith('.json.gz'):
        logging.error("Can only accept source files in JSON compressed format, for the moment")
        return
    # read as single column
    df = pd.read_csv(f'{src_file}', header=None, names=['json_value'],sep='\0')
    df.to_parquet(src_file.replace('.json.gz', '.parquet'), index=False)

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="data_ingestion_github",
    schedule_interval="30 * * * *",
    start_date = datetime(2022,3,21),
    default_args=default_args,
    catchup=True,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sSLf {dataset_url} > {path_to_local_home}/{dataset_file}"
    )

    format_to_parquet_task = PythonOperator(
        task_id="format_to_parquet_task",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_file": f"{path_to_local_home}/{dataset_file}",
        },
    )


    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{parquet_file}",
            "local_file": f'{path_to_local_home}/{parquet_file}',
        },
    )

    clean_up_files_task = BashOperator(
        task_id="clean_up_files_task",
        bash_command=f"rm {path_to_local_home}/{dataset_file} {path_to_local_home}/{parquet_file}"
    )

    download_dataset_task >> format_to_parquet_task >> local_to_gcs_task >> clean_up_files_task
