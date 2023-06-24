# coding:utf-8
import datetime
import json
import requests
import re

# state = 0
#
# re_dict = {'key':True,'fuck':True}
# for key in re_dict:
#     print(key,type(key))
# with open("D:/hina bot/hinabot/.venv/Lib/site-packages/nonebot/plugins/mazui_study/resource/mazui_state.json", 'r',
#           encoding='utf-8') as f:
#     params = json.load(f)
#
#     for key, value in dict:
#         params[key] = value


# def mod_json_data(state: str, value: bool) -> json:
#     with open("D:/hina bot/hinabot/.venv/Lib/site-packages/nonebot/plugins/mazui_study/resource/mazui_state.json", 'r',
#               encoding='utf-8') as f:
#         params = json.load(f)
#
#         params[state] = value
#
#         return params
#
# def write_study(params: json) -> None:
#         with open("D:/hina bot/hinabot/.venv/Lib/site-packages/nonebot/plugins/mazui_study/resource/mazui_state.json",
#                   'w', encoding='utf-8') as f:
#             json.dump(params, f, indent=4)
#
#
# params = mod_json_data('mazui_state',False)
# write_study(params)
# with open("D:/hina bot/hinabot/.venv/Lib/site-packages/nonebot/plugins/mazui_study/resource/mazui_state.json", 'w',
#           encoding='utf-8') as f:
#     dict1 = {
#         "mazui_state": False
#
#     }
#     dict2 = {
#         "mazui_state": True,
#         "zxh_state": True
#     }
#
#     if state:
#         json.dump(dict1, f, indent=4)
#     else:
#         json.dump(dict2, f, indent=4)
class WebSpider(object):
    def __init__(self):
        self.url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzk0NjA5MjEzNQ==&action=getalbum&album_id=2644861174949462016&scene=173&from_msgid=2247515120&from_itemidx=2&count=3&nolastread=1#wechat_redirect"

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'

                          ' Chrome/92.0.4515.107 Safari/537.36'
        }

    def parse(self):

        res = requests.get(self.url)
        mre = re.search(r"http://mp.weixin.qq.com.*",res.text)
        res = requests.get(mre.group().strip("\""))

        re_pic = r"https://mmbiz.qpic.cn/mmbiz_png/.*"
        mre = re.findall(r"\"https://mmbiz.qpic.cn/mmbiz_png/.*?\"",res.text)
        return mre

    def save_all_pic(self):

        list_pic = self.parse()

        for index,url in enumerate(list_pic):
            url : str = url.strip("'").strip("\"")
            self.save_pic(url,str(index)+"math.png")

    def save_pic(self,url,name):

        res = requests.get(url)
        print(len(res.content))
        with open(f"./resource/{name}",'wb') as f:
            f.write(res.content)


ws = WebSpider()

print(ws.save_all_pic())

