# Data Engineering Project

## Problem Statement

We would like to understand what kind of activity Github sees on a daily basis. In additon we want to determine which projects are the most popular at Github.

The dataset chosen is [GitHub Archive](https://www.gharchive.org/).

## Project Description

This project implements an ELT pipeline extracting the data from github, uploading to GCS and then transformed using BigQuery. A dashboard is created to illustrate the findings.

## Setup

This project is run on a compute engine instance. You must installed the following tools:

- Python 3.9
- Terraform
- Docker + Docker compose
- git

The startup.sh script will help you install a few of these components

### 1. Environment Setup

- [Python 3.9](https://linuxize.com/post/how-to-install-python-3-9-on-debian-10/)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- [Docker](https://docs.docker.com/engine/install/debian/)
- [Docker Compose](https://docs.docker.com/compose/install/)


[Setup Video](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

[GCP Instructions](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_1_basics_n_setup/1_terraform_gcp/2_gcp_overview.md#initial-setup)

Create a .google/credentials/google_credentials.json with your service account

### 2. Clone Repo

With git installed in the repo. Clone this project and cd to the project folder

### 3. Run Terraform

Apply terraform to create GCS bucket and Bigquery

### 4. Setup Airflow

Update the docker compose file with your GCP paths and credentials. In the airflow folder run docker compose up. Start the DAGS!

- github_ingestion_gcs_dag
    - This ingests data converts to parquet to GCS
- gcs_to_bq_dag
    - Uploads creates table in bigquery
- dbt_run
    - Runs dbt models







