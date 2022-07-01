import boto3

def connect_to_s3():
        return boto3.resource('s3', aws_access_key_id='', aws_secret_access_key='')

def upload_file_s3(**kwargs):
    conn = connect_to_s3()
    conn.meta.client.upload_file(
               Filename = f"/opt/airflow/data/cho-tot-{kwargs['prev_ds']}.parquet", 
               Bucket = 'chotot-data', 
               Key = f"cho-tot-{kwargs['prev_ds']}.parquet")


if __name__ == '__main__':
    pass
    # connect_to_s3()
    # print('Connected!')