from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from kafka_producer import download_cat_image_data

# Default arguments for the DAG
default_args = {
    "owner": "admin",
    "depends_on_past": False,
    "start_date": datetime(2023, 8, 18),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    "schedule_interval": timedelta(seconds=30),
}

# Create a DAG instance
dag = DAG(
    "cat_photo_dag",
    default_args=default_args,
    description="DAG to fetch cat photos",
    schedule_interval=timedelta(seconds=30),
    catchup=False,
)

# Define the tasks

# Task 1:
fetch_cat_photo_task = PythonOperator(
    task_id="fetch_cat_photo",
    python_callable=download_cat_image_data,
    dag=dag,
)

# Set the task dependencies
fetch_cat_photo_task
