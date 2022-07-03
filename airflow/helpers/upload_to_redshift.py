import os
import sys
import io
import boto3
from dotenv import load_dotenv,find_dotenv
import sqlalchemy as sa
import pandas as pd

load_dotenv(find_dotenv())

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
USERNAME = os.getenv('redshift_username')
PASSWORD = os.getenv('redshift_password')
HOST = os.getenv('redshift_cluster_hostname')
ROLE = os.getenv('redshift_role')
ACCOUNT_ID = os.getenv('account_id')
BUCKET = os.getenv('bucket')
DATABASE = 'cho_tot_db'
PORT = 5439





#depreciate
# region_path = f's3://{BUCKET}/region.parquet'
# role_string = f'arn:aws:iam::{ACCOUNT_ID}:role/{ROLE}'

def copy_s3_to_redshift(file_name, engine, table_name):

    buffer = io.BytesIO()
    s3 = boto3.resource('s3')
    object = s3.Object(BUCKET,file_name)
    object.download_fileobj(buffer)
    df = pd.read_parquet(buffer)
    df.to_sql(table_name, con=engine, index = False, if_exists='replace', method='multi')

def insert_s3_to_redshift(file_name, engine, table_name):
    buffer = io.BytesIO()
    s3 = boto3.resource('s3')
    object = s3.Object(BUCKET,file_name)
    object.download_fileobj(buffer)
    df = pd.read_parquet(buffer)
    cols = ['account_id','ad_id','region_v2','area_v2','ward_name','street_name','category','list_time','latitude','longitude','owner','length','width','size','price','rooms','toilets']
    df = df[cols]
    df.to_sql(table_name, con=engine, index = False, if_exists='append', method='multi')

if __name__ == '__main__':
    
    engine = sa.create_engine(f"redshift+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
    # rs_conn = psycopg2.connect(dbname = DATABASE, user = USERNAME, password = PASSWORD, host = HOST, port = PORT)
    # cursor = rs_conn.cursor()

    copy_s3_to_redshift('region.parquet', engine, 'region')
    copy_s3_to_redshift('area.parquet', engine, 'area')
    copy_s3_to_redshift('category.parquet', engine, 'category')
    insert_s3_to_redshift(f'cho-tot-{sys.argv[1]}.parquet', engine, 'posts')
