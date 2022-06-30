import os
import logging
import requests
import pandas as pd

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import pyarrow.csv as pv
import pyarrow.parquet as pq
from datetime import datetime


dataset_file = "yellow_tripdata_2021-01.csv"
dataset_url = f"https://s3.amazonaws.com/nyc-tlc/trip+data/{dataset_file}"
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
parquet_file = dataset_file.replace('.csv', '.parquet')

def get_area(path):
    id, region_id, name, url_name, lat, longt = [],[],[],[],[],[]
    url  = 'https://gateway.chotot.com/v1/public/web-proxy-api/loadRegions'
    response = requests.get(url)
    r_json = response.json()
    regions = r_json['regionFollowId']['entities']['regions']
    for region_idx in regions.keys():
        region = regions[region_idx]
        area = region['area']
        for area_id, area_value in area.items():
            id.append(area_id)
            region_id.append(region_idx)
            name.append(area_value['name'])
            url_name.append(area_value['name_url'])
            if len(area_value['geo'].split(',')) == 2:
                lat.append(area_value['geo'].split(',')[0])
                longt.append(area_value['geo'].split(',')[1])
            else:
                lat.append('N/A')
                longt.append('N/A')
        
    result = pd.DataFrame({
        'id' : id,
        'region_id' : region_id,
        'name' : name,
        'url_name' : url_name,
        'lat' : lat,
        'long' : longt
    })
    result.to_csv(path)
    print(f'save file to {path}')
    # return result


def get_region(path):
    id, name, url_name, lat, longt = [],[],[],[],[]
    url  = 'https://gateway.chotot.com/v1/public/web-proxy-api/loadRegions'
    response = requests.get(url)
    r_json = response.json()
    regions = r_json['regionFollowId']['entities']['regions']
    for region_id in regions.keys():
        region = regions[region_id]
        id.append(region['id'])
        name.append(region['name'])
        url_name.append(region['name_url'])
        lat.append(region['geo'].split(',')[0])
        longt.append(region['geo'].split(',')[1])

    result = pd.DataFrame({
        'id' : id,
        'name' : name,
        'url_name' : url_name,
        'lat' : lat,
        'long' : longt
    })
    result.to_csv(path)
    print('Save region to {path}')

def format_to_parquet(src_file):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace('.csv', '.parquet'))

# default_args = {
#     "owner": "airflow",
#     "start_date": days_ago(1),
#     "depends_on_past": False,
#     "retries": 1,
# }

# with DAG(
#     dag_id="test_parquet",
#     schedule_interval="@daily",
#     default_args=default_args,
#     catchup=False,
#     max_active_runs=1,
#     tags=['dtc-de'],
# ) as dag:

#     # get_area_task = PythonOperator(
#     #     task_id = "get_area_task",
#     #     python_callable= get_area,
#     #     op_kwargs = {
#     #         "path": f"{path_to_local_home}/area.csv"
#     #     }
#     # )

#     # get_region_task = PythonOperator(
#     #     task_id = "get_region_task",
#     #     python_callable= get_area,
#     #     op_kwargs = {
#     #         "path": f"{path_to_local_home}/region.csv"
#     #     }
#     # )
#     download_dataset_task = BashOperator(
#         task_id="download_dataset_task",
#         bash_command=f"curl -sSL {dataset_url} > {path_to_local_home}/{dataset_file}"
#     )


#     format_to_parquet_task = PythonOperator(
#         task_id="format_to_parquet_task",
#         python_callable=format_to_parquet,
#         op_kwargs={
#             "src_file": f"{path_to_local_home}/area.csv",
#         },
#     )
default_args = {
    "owner": "airflow",
    "start_date": days_ago(10),
    "depends_on_past": False,
    "retries": 1,
}
def test_df(arr):
    print(pd.Series(arr))
def test_dt(date):
    print(date > datetime(2021, 6, 29, 13, 33, 44) )

# NOTE: DAG declaration - using a Context Manager (an implicit way)
with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="wget",
        bash_command=f"echo hello"
    )

    format_to_parquet_task = PythonOperator(
        task_id="format_to_parquet_task",
        python_callable=test_df,
        op_kwargs={
            "arr":[1,2,3,4],
        },
    
        

    ),
    get_area_task = PythonOperator(
        task_id = "get_area_task",
        python_callable= get_area,
        op_kwargs = {
            "path": f"{path_to_local_home}/area.csv"
        }
    )
    list_all_file = BashOperator(
        task_id="list_all_file",
        bash_command=f"ls {path_to_local_home}"
    )

# get_area_task >> get_region >> format_to_parquet_task





download_dataset_task  >> format_to_parquet_task >> get_area_task >> list_all_file

