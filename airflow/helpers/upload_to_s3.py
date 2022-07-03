from http.client import ImproperConnectionState
import boto3
import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())
BUCKET = os.getenv('bucket')
path_to_local_home = "/opt/airflow/"
import logging

def connect_to_s3():
        return boto3.resource('s3')

def upload_file_s3(**kwargs):
    files = {f'{path_to_local_home}data/region.parquet':'region.parquet',
            f'{path_to_local_home}data/area.parquet': 'area.parquet',
            f'{path_to_local_home}data/category.parquet':'category.parquet',
            f"{path_to_local_home}data/cho-tot-{kwargs['prev_ds']}.parquet" :f"cho-tot-{kwargs['prev_ds']}.parquet" }
    s3 = connect_to_s3()
    for local_name, s3_name in files.items():
        s3.meta.client.upload_file(
                Filename = local_name, 
                Bucket = f'{BUCKET}', 
                Key = s3_name)
        logging.info(f'{local_name} : {s3_name}')


if __name__ == '__main__':
    pass
    # connect_to_s3()
    # print('Connected!')