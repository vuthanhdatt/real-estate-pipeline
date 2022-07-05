import os
import logging

import pandas as pd
import sys




sys.path.insert(0, '/opt/airflow/helpers')

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from datetime import datetime
from extract_chotot_data import get_area, get_region, get_all_posts, get_category
from upload_to_s3 import upload_file_s3


path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")


with DAG(
    dag_id="dag_daily",
    schedule_interval="@daily",
    # default_args=default_args,
    start_date= datetime(2022,7,1),
    # max_active_runs=1,
    tags=['real_estae_pipeline'],
) as dag:

    get_area_task = PythonOperator(
        task_id="get_area_task",
        python_callable = get_area,
        op_kwargs = {
            "path" : f"{path_to_local_home}/data/area.parquet"
        }
    )

    get_region_task = PythonOperator(
        task_id="get_region_task",
        python_callable=get_region,
        op_kwargs = {
            "path" : f"{path_to_local_home}/data/region.parquet"
        })
        
    get_cat_task = PythonOperator(
        task_id="get_cat_task",
        python_callable=get_category,
        op_kwargs = {
            "path" : f"{path_to_local_home}/data/category.parquet"
        }
    )

    get_post_task = PythonOperator(
        task_id= 'get_post_task',
        python_callable= get_all_posts, 
        provide_context = True
    )

    list_all_file = BashOperator(
        task_id="list_all_file",
        bash_command='ls -a'
    )

    upload_to_s3 = PythonOperator(
        task_id= 'upload_to_s3',
        python_callable= upload_file_s3, 
        provide_context = True

    )

    upload_to_redshift = BashOperator(
        task_id= 'upload_to_redshift',
        bash_command='python /opt/airflow/helpers/upload_to_redshift.py "{{ prev_ds }}"'
    )



get_area_task  >> get_region_task >> get_cat_task >> get_post_task >> list_all_file >> upload_to_s3 >> upload_to_redshift

