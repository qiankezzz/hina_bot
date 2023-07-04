import datetime
import json
import os
import asyncio
from typing import List
from httpx import AsyncClient





async def load_pic(num: int,sort: str='random'):
        
        async with AsyncClient(verify=False) as client:
            url = "https://iw233.cn/api.php"
            params = {
                'sort': sort,
                'type': 'json',
                'num': str(num),
            }
            res = await client.get(url, params=params)
            url_list = res.json()['pic']
            if os.path.exists("./data/color_image"):
                for index, url in enumerate(url_list):
                    res = await client.get(url, timeout=120)
                    with open(f"./data/color_image/{index}.png", 'wb') as f:
                        f.write(res.content)
            else:
                os.makedirs("./data/color_image")
                await load_pic(num)


async def write_date():
        data_dir = "./data/color_image/data/"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        with open(data_dir+"cd.json",'w',encoding='utf-8') as f:
            CD = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dict = {
                "CD":str(CD)
            }
            json.dump(dict, f, indent=4)


async def read_date() -> bool:
        data_dir = "./data/color_image/data/"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            with open(data_dir+"cd.json",'w',encoding='utf-8') as f:
                json.dump({}, f, indent=4)
        with open(data_dir+"cd.json",'r',encoding='utf-8') as f:
            content = json.load(f)
        if not content:
            return True
        else:
            CD = content['CD']
            old_CD = datetime.datetime.strptime(CD,'%Y-%m-%d %H:%M:%S')
            now_CD = datetime.datetime.now()
            if (now_CD - old_CD).seconds > 20:
                return True
            return False
        

if __name__ == '__main__':
     print(dir(json))