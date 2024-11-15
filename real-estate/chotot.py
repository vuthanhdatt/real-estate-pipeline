
import requests
import pandas as pd
from datetime import datetime

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'ct-fingerprint': '8816ee08-f137-4940-8d39-0d74f15e19fb',
    'ct-platform': 'web',
    'origin': 'https://www.nhatot.com',
    'priority': 'u=1, i',
    'referer': 'https://www.nhatot.com/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
}


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
    result.to_csv(path, index=False)


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
        result.to_csv(path, index=False)
    else:
        return result
    
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
    result.to_csv(path, index=False)

if __name__ == "__main__":
    area_path = 'data/area.csv'
    get_area(area_path)
    region_path = 'data/region.csv'
    get_region(region_path)
    category_path = 'data/category.csv'
    get_category(category_path)
    print('Done!')