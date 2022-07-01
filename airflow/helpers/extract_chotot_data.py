import requests
import pandas as pd
from datetime import datetime



def get_area(path):
    id, region_id, name, url_name, lat, long = [],[],[],[],[],[]
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
                long.append(area_value['geo'].split(',')[1])
            else:
                lat.append('N/A')
                long.append('N/A')
        
    result = pd.DataFrame({
        'id' : id,
        'region_id' : region_id,
        'name' : name,
        'url_name' : url_name,
        'lat' : lat,
        'long' : long
    })
    result.to_csv(path)
    # return result

def get_region(path):
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
    result.to_parquet(path)
    
    # return result

def get_category(path):
    id, name = [], []
    url = 'https://gateway.chotot.com/v5/public/chapy-pro/categories'
    r = requests.get(url)
    cat = r.json()
    for sub_cat in cat['categories'][0]['subcategories']:
        id.append(sub_cat['id'])
        name.append(sub_cat['name'])
    result = pd.DataFrame({
        'id' : id,
        'name' : name,
    })
    result.to_parquet(path)

# def get_post(posts):
#     account_id = []
#     ad_id = []
#     area_id = []
#     region_id = []
#     ward_name = []
#     street_name = []
#     body = []
#     cat_id = []
#     date = []
#     lat = []
#     long = []
#     owner = []
#     length = []
#     width = [] 
#     size = []
#     price = [] 
#     room = [] 
#     toilets = []
#     for post in posts:
#         account_id.append(post['account_id'])
#         ad_id.append(post['ad_id'])
#         region_id.append(post.get('region_v2','N/A'))
#         area_id.append(post.get('area_v2','N/A'))
#         ward_name.append(post.get('ward_name','N/A'))
#         street_name.append(post.get('street_name','N/A'))
#         cat_id.append(post.get('category','N/A'))
#         date.append(post.get('list_time','N/A'))
#         body.append(post.get('body','N/A'))
#         lat.append(post.get('latitude','N/A'))
#         long.append(post.get('longitude','N/A'))
#         owner.append(post.get('owner','N/A'))
#         length.append(post.get('length','N/A'))
#         width.append(post.get('width','N/A'))
#         size.append(post.get('size','N/A'))
#         price.append(post.get('price','N/A'))
#         room.append(post.get('rooms','N/A'))
#         toilets.append(post.get('toilets', 'N/A'))
#     result = pd.DataFrame({
#         'account_id': account_id, 
#         'ad_id':ad_id, 
#         'area_id':area_id, 
#         'region_id':region_id,
#         'ward_name':ward_name, 
#         'street_name':street_name, 
#         'body':body, 
#         'cat_id':cat_id, 
#         'date':date, 
#         'lat':lat, 
#         'long':long, 
#         'owner':owner, 
#         'length':length, 
#         'width':width, 
#         'size':size, 
#         'price':price, 
#         'room':room, 
#         'toilets':toilets
#     })
#     return result

# def get_post_region(region, date_time):
#   start = 0
#   url = f'https://gateway.chotot.com/v1/public/ad-listing?region_v2={region}&cg=1000&o=0&st=s,k&limit=100&key_param_included=true'
#   r = requests.get(url)
#   r_json = r.json()
#   total = r_json['total']
#   result = get_post(r_json['ads'])
#   while start < 500:
#     start += 100
#     url = f'https://gateway.chotot.com/v1/public/ad-listing?region_v2={region}&cg=1000&o={str(start)}&st=s,k&limit=100&key_param_included=true'
#     r = requests.get(url)
#     r_json = r.json()
#     if date_time == 'all':
#         result = result.append(get_post(r_json['ads']))
#         print(f'Load {start}')
#     else:
#         if datetime.utcfromtimestamp(r_json['ads'][0]['list_time']/1000) < date_time:
#             break
#         else:
#             result = result.append(get_post(r_json['ads']))
#             print(f'Load {start}')
#   return result

def get_post_region(region, **kwargs):
    start = 0
    start_date = datetime.strptime(kwargs['prev_ds'], '%Y-%m-%d')
    end_date = datetime.strptime(kwargs['ds'], '%Y-%m-%d')
    path = f"/opt/airflow/data/cho-tot-{kwargs['prev_ds']}.parquet"
    result = pd.DataFrame()  
    while start < 10000:
        url = f'https://gateway.chotot.com/v1/public/ad-listing?region_v2={region}&cg=1000&o={str(start)}&st=s,k&limit=100&key_param_included=true'
        r = requests.get(url)
        r_json = r.json()
        lastest_unix_time = datetime.utcfromtimestamp(r_json['ads'][-1]['list_time']/ 1000)
        ealiest_unix_time = datetime.utcfromtimestamp(r_json['ads'][0]['list_time']/ 1000)
        if ealiest_unix_time < start_date:
            break
        else:
            for ad in r_json['ads']:
                ad.pop('params', None)
                ad.pop('videos', None)
                for k, v in ad.items():
                    ad[k] = [v]
                df = pd.DataFrame(ad)
                result = pd.concat([result, df])
        start += 100
    result['list_time'] = pd.to_datetime(result['list_time']/1000,unit='s')
    
    result = result[result['list_time'].between(start_date, end_date)]
    result.to_parquet(path,use_deprecated_int96_timestamps=True)
    # result.to_csv(path)




def save_to_csv(df, path):
    df.to_csv(path)
    
if __name__ == '__main__':

    pass
    # from datetime import datetime
    # get_post_region('9053','2022-06-28','2022-06-29', '/home/vuthanhdatt/test_airflow/dl.csv' )
    # save_to_csv(df,'/home/vuthanhdatt/test_airflow/dl.csv')