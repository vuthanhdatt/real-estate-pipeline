from aiolimiter import AsyncLimiter
import asyncio
import logging
import aiohttp
import json
import requests
import pandas as pd
import os
logging.basicConfig(format='%(asctime)s - %(process)d - %(thread)d - %(message)s', level=logging.INFO)

# allow for 100 concurrent entries within a 30 second window
rate_limit = AsyncLimiter(3, 1)

area_df = pd.read_csv('data/area.csv')
area_df = area_df[area_df['region_id'] == 13000][['id','name']]
area = area_df.set_index('id')['name'].to_dict()
cate = {'1010':"Căn hộ/Chung cư", '1020':"Nhà ở",'1040':"Đất"}


async def get_ads(start, area_id, cate_id):
    url = f"https://gateway.chotot.com/v1/public/ad-listing?region_v2=13000&area_v2={area_id}&cg={cate_id}&o={start}&page=1&st=s,k&limit=50&include_expired_ads=true&key_param_included=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if response.status != 200:
                logging.error(f'Error at {start} with status code {response.status} of {cate[cate_id]} in {area[area_id]}')
                raise Exception(f'Error at {start} with status code {response.status} of {cate[cate_id]} in {area[area_id]}')
            path = f'data/json/13000/{area_id}/{cate_id}'
            with open(f'{path}/{start}.json', 'w') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

async def some_coroutine(i, area_id, cate_id):
    async with rate_limit:
        logging.info(f'Get item of {cate[cate_id]} from {i} to {i+50} in {area[area_id]}')
        await get_ads(i, area_id, cate_id)

if __name__ == '__main__':


    loop = asyncio.get_event_loop()

    for cate_id, cate_name in cate.items():
        for area_id, area_name in area.items():
            path = f'data/json/13000/{area_id}/{cate_id}'
            if not os.path.exists(path):
                os.makedirs(path)
            logging.info(f'Get {cate_name} in {area_name}')
            url = f"https://gateway.chotot.com/v1/public/ad-listing?region_v2=13000&area_v2={area_id}&cg={cate_id}&o=0&page=1&st=s,k&limit=50&include_expired_ads=true&key_param_included=true"
            response = requests.get(url)
            try:
                total_ads = response.json()['total']
                logging.info(f'Total ads: {total_ads} in {area_name} of {cate_name}')
                loop.run_until_complete(asyncio.gather(*[some_coroutine(i, area_id, cate_id) for i in range(0, total_ads, 50)]))
            except Exception as e:
                logging.info(f'{cate_name} in {area_name} do not have any result')