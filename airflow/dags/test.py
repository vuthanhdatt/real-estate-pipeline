import sys
sys.path.insert(0, '/home/vuthanhdatt/real-estate-pipeline/airflow/helpers')

from extract_chotot_etl import get_area

if __name__ == '__main__':
    print(get_area())