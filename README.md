# real-estate-pipeline
A data pipeline to extract Vietnam real estate data from [Chợ tốt nhà](https://nha.chotot.com/).

## Architecture


- Extract data from [Chợ tốt nhà](https://nha.chotot.com/) (Extract)
- Load into [AWS S3](https://aws.amazon.com/s3/) (Data lake)
- Transfom and load into [AWS Redshift](https://aws.amazon.com/redshift/) (Data warehouse)
- Transform using [dbt](https://www.getdbt.com/) (Transform)
- Create [Google Data Studio](https://datastudio.google.com/) Dashboard (Apply)
- Orchestrate pipeline with [Airflow](https://airflow.apache.org/) in [Docker](https://www.docker.com/) 
- Create AWS resources with [Terraform](https://www.terraform.io/) (Infrastructure)


## Extract data
Chotot don't have public API so I inspect their website and found out some hidden API. Data extract include region, area, category and all the posting. All the code for extract data in [`helper/extract_chotot_data.py`](https://github.com/vuthanhdatt/real-estate-pipeline/blob/main/airflow/helpers/extract_chotot_data.py) file. For example, to get all region.
```python
def get_region(path, save=True):
    id, name, url_name, lat, long = [],[],[],[],[]
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
        long.append(region['geo'].split(',')[1])

    result = pd.DataFrame({
        'id' : id,
        'name' : name,
        'url_name' : url_name,
        'lat' : lat,
        'long' : long
    })
    if save:
        result.to_parquet(path, index=False)
    else:
        return result
```
## Load into S3

S3 will be data lake in this data pipeline, it store all raw data I just extract from chotot. To load data into S3, I use [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html). The data we extract will be daily upload to S3 bucket. For example,

image

## Load into Redshift
Since the data we extract is raw, I transform it a little bit and load into data warehouse - Redshift. 

img

## Transfom with dbt

I use dbt to transform my data in Redshift, since the data quite simple, this step not really necessary. The data after transform will load back to Redshift.

img


## Docker & Airflow
I'm going to run my pipeline daily, for demonstration purposes, although this could be changed at a later point. Each day, the pipeline above will be running to ensure all the new posts will be update to my data warehouse.

