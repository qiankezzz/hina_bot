# coding:utf-8
import json
import os
import requests
class WebSpider(object):

    def __init__(self):
        self.url = 'https://bbs-api.mihoyo.com/post/wapi/getForumPostList?forum_id=49'

        self.headers = {

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'

                          ' Chrome/92.0.4515.107 Safari/537.36'

        }

    def parse(self) -> dict:

        cos_dict = {}

        res = requests.get(self.url,headers=self.headers).content.decode('utf-8')
        res = json.loads(res)
        res = res['data']['list']

        subject_name = [i['post']['subject'] for i in res]
        cover_url = [i['post']['images'] for i in res]

        for name,url in zip(subject_name,cover_url):
            cos_dict[name] = url

        return cos_dict

    def save_pic(self) -> str:

        cos_dict = self.parse()
        
        for name in cos_dict:
            url_list = cos_dict[name]
            for id,url in enumerate(url_list):
                pic_type = url.split('.')[-1]
                res = requests.get(url,headers=self.headers).content
                path = r"C:\hina bot\hinabot2\.venv\Lib\site-packages/nonebot\plugins\genshin_cos/resource/{0}.{1}".format(name+"_"+str(id),pic_type)
                if not os.path.exists(path):
                    with open(path,'wb') as f:
                        f.write(res)
                yield path
                


if __name__ == '__main__':
    ws = WebSpider()
    next(ws.save_pic())
    next(ws.save_pic())
