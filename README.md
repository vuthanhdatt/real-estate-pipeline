# Vietnam Real Estate Data Pipeline
A data pipeline to extract Vietnam real estate data daily from [Chợ tốt nhà](https://nha.chotot.com/).

## Architecture

![Architecture](https://github.com/vuthanhdatt/real-estate-pipeline/blob/main/img/architecture.png)


- Extract data from [Chợ tốt nhà](https://nha.chotot.com/) (Extract)
- Load into [AWS S3](https://aws.amazon.com/s3/) (Data lake)
- Transfom and load into [AWS Redshift](https://aws.amazon.com/redshift/) (Data warehouse)
- Transform using [dbt](https://www.getdbt.com/) (Transform)
- Create [Google Data Studio](https://datastudio.google.com/) Dashboard (Apply)
- Orchestrate pipeline with [Airflow](https://airflow.apache.org/) in [Docker](https://www.docker.com/) 
- Create AWS resources with [Terraform](https://www.terraform.io/) (Infrastructure)

## Project structure
```bash

├── airflow
│   ├── Dockerfile
│   ├── dags
│   │   └── daily_elt_pipeline.py
│   ├── docker-compose.yaml
│   ├── helpers
│   │   ├── extract_chotot_data.py
│   │   ├── upload_to_redshift.py
│   │   └── upload_to_s3.py
│   └── requirements.txt
├── dbt
│   ├── dbt-project.yml
│   └── models
│       ├── schema.yml
│       └── transform.sql
│   
├── terraform
│    ├── main.tf
│    ├── output.tf
│    └── variable.tf
├── .gitignore
├── README.md
```

## Extract data
Chotot doesn't have public API so I inspect their website and found out some hidden API. Data extract include region, area, category and all the posting. All the code for extract data in [`extract_chotot_data.py`](https://github.com/vuthanhdatt/real-estate-pipeline/blob/main/airflow/helpers/extract_chotot_data.py) file. For example, to get all region.
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

S3 will be data lake in this data pipeline, it store all raw data I just extract from chotot The data we extract will be daily upload to S3 bucket, store in `parquet` file type.


![s3](https://github.com/vuthanhdatt/real-estate-pipeline/blob/main/img/s3.png)

## Load into Redshift
Since the data we extract is raw, I transform it a little bit and load into data warehouse - Redshift. 

![s3](https://github.com/vuthanhdatt/real-estate-pipeline/blob/main/img/redshift.png)




## Docker & Airflow
I'm going to run my pipeline daily, for demonstration purposes, although this could be changed at a later point. Each day, the pipeline above will be running to ensure all the new posts will be update to my data warehouse.

We need to build the image first

```bash
docker-compose build
docker-compose up airflow-init
```
After building the image, we can use `docker-compose up` to start Airflow to run all the tasks for this pipeline. 

![aiflow](https://github.com/vuthanhdatt/real-estate-pipeline/blob/main/img/airflow.png)

## Transfom with dbt

I use dbt to transform my data in Redshift, since the data quite simple, this step not really necessary.

![dbt](https://github.com/vuthanhdatt/real-estate-pipeline/blob/main/img/dbt.png)

The data after transform will load back to Redshift.

![back_redshift](https://github.com/vuthanhdatt/real-estate-pipeline/blob/main/img/back_redshift.png)

## Infrastructure with terraform

Again, this step quite overkill for small project like this, but using terraform is a good way to create AWS resources. I use terraform to create AWS resources S3, Redshift, IAM.

## Visualize with Google Data Studio

Finally, I use Google Data Studio to visualize the data. You can take a look [here](https://datastudio.google.com/reporting/8c0c01ef-931c-4ebb-b3e6-b6444f8a8041).
