# coding:utf-8
import json
import time

import requests
import re
import os
from pathlib import Path

class daily_math(object):

    def __init__(self,title,url):
        self.title = title
        self.url = url

    def __dict__(self):
        return {'title':self.title, 'url':self.url}






class WebSpider(object):
    
    def __init__(self):
        # 考研每日一题

        self.url = f"https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz=Mzk0NjA5MjEzNQ==&album_id=2644861174949462016&count=1140&f=json"

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.197.400 QQBrowser/11.7.5287.400',
            'referer': 'https://www.bilibili.com/',
            'cookies': 'buvid4=3E6627AC-7EED-9FDE-9E34-D595C8A096F690804-022061816-cWZGbE4cldr4uOyI4FoEIQ==; b_nut=1675737874; buvid3=6849DF18-E869-B243-C927-D74ADFBB8A7873882infoc; hit-new-style-dyn=0; _uuid=C66657110-852E-296B-107C3-26164EEDBB4A76730infoc; hit-dyn-v2=1; buvid_fp_plain=undefined; SESSDATA=acfe2426,1691289889,9eb56*22; bili_jct=3a7307e4ce5390a173ad5355d18003b2; DedeUserID=176454210; DedeUserID__ckMd5=6b3ad69123d48aac; sid=71vgt7bi; CURRENT_FNVAL=4048; rpdid=|(J~RYul~|km0J\'uY~l~J)Rkk; nostalgia_conf=-1; i-wanna-go-back=-1; b_ut=5; LIVE_BUVID=AUTO2016760033322926; header_theme_version=CLOSE; CURRENT_QUALITY=80; CURRENT_PID=62a4a130-cd1f-11ed-9f41-1b6f57bc6201; FEED_LIVE_VERSION=V8; PVID=1; home_feed_column=5; fingerprint=b71c352af063eaa5e333989d4348d18b; buvid_fp=b71c352af063eaa5e333989d4348d18b; share_source_origin=copy_web; bp_video_offset_176454210=787628381643473000; innersign=1; bsource=search_baidu; browser_resolution=1708-818; b_lsid=C1695973_187ACE8C1BF'
        }


    # def parse(self) -> tuple:
    #
    #     '''
    #     0:返回列表 包含所有该日网页所有图片的url
    #     1:返回一个字符串 为该日标题
    #     2:返回一个列表 请求得到的所有url
    #     3:返回一个列表 请求得到的所有标题，与上述url一一对应
    #     '''
    #
    #     res = requests.get(self.url)
    #
    #     data_link_re = r"(data-link=)(.*)"
    #     data_title_re = r"(data-title=)(.*)"
    #
    #     list_link : list = [url[1].strip("\"") for url in re.findall(data_link_re,res.text)]
    #     list_title : list = [title[1].strip("\"") for title in re.findall(data_title_re,res.text)]
    #
    #     res = requests.get(list_link[0])
    #     mre : list = re.findall(r"\"https://mmbiz.qpic.cn/mmbiz_png/.*?\"",res.text)
    #
    #     return mre,list_title[1],list_link,list_title

    def parse(self) -> tuple:

        '''
               0:返回列表 包含所有该日网页所有图片的url
               1:返回一个字符串 为该日标题
               2:返回一个列表 请求得到的所有url
               3:返回一个列表 请求得到的所有标题，与上述url一一对应
               4:返回数字列表
         '''

        list_math = requests.get(self.url).json()["getalbum_resp"]['article_list']
        list_url = [url['url'] for url in list_math]
        list_title = [title['title'] for title in list_math]
        list_num = [num['pos_num'] for num in list_math]


        return list_url[0], list_title[0], list_url, list_title, list_num

    def parse_loop(self):

        list_math = requests.get(self.url).json()["getalbum_resp"]['article_list']
        list_url = [url['url'] for url in list_math]
        list_title = [title['title'] for title in list_math]
        list_itemidx = [itemidx['itemidx'] for itemidx in list_math]
        list_msgid = [msgid['msgid'] for msgid in list_math]

        while "98｜ 这道题的正确率仅 40%， 多半都是计算失误" not in list_title:
            params = {
                'begin_msgid': list_msgid[-1],
                'begin_itemidx': list_itemidx[-1]
            }
            last_list_math = requests.get(self.url, params=params).json()["getalbum_resp"]['article_list']
            last_list_url = [url['url'] for url in last_list_math]
            last_list_title = [url['title'] for url in last_list_math]
            last_list_msgid = [url['msgid'] for url in last_list_math]
            last_list_itemidx = [url['itemidx'] for url in last_list_math]
            list_url.extend(last_list_url)
            list_title.extend(last_list_title)
            list_msgid.extend(last_list_msgid)
            list_itemidx.extend(last_list_itemidx)
        for title, url in zip(list_title, list_url):
            self.write(daily_math(title=title, url=url))

    def save_all_pic(self,index: int = 0) -> tuple:

        """
        保存题目图片
        并返回元祖
        0:路径 : str
        1:标题名 : str
        2:补充路径 : str
        3:链接 : str
        """
        list_pic : list[str] = self.parse()[2]
        list_name: str = self.parse()[3][index]
        # last_name = self.parse()[3][index+1]
        list_pic[index] = list_pic[index].replace("amp;","")
        res = requests.get(list_pic[index],headers=self.headers)

        today_pic: str = re.findall(r"(今日习题.*?)(data-src=\")(.*?)\"",res.text)[0][2]
        try:
            today_extra: str = re.findall(r"(知识.*?)(data-src=\")(.*?)\"",res.text)[0][2]
        except:
            today_extra : str = None
        # list_pic: list = re.findall(r"\"https://mmbiz.qpic.cn/mmbiz_png/.*?\"", res.text)

        url: str = today_pic
        url_extra: str = today_extra
        name = f"{list_name}.png"
        name_extra = f"{list_name}_extra.png"
        path = os.path.abspath(f"./data/daily_math")

        if not os.path.exists(path):
            os.makedirs(path)

        if self.save_pic(url, name) and self.save_pic(url_extra,name_extra):
            return os.path.abspath(f"./data/daily_math/{name}"), list_name, os.path.abspath(f"./data/daily_math/{name_extra}"), list_pic[index]
        return os.path.abspath(f"./data/daily_math/{name}"), list_name, None, list_pic[index]

        # for url in list_pic:
        #     url : str = url.strip("'").strip("\"")
        #     name = f"{list_name}.png"
        #     path = os.path.abspath(f"./data/daily_math")
        #
        #     if not os.path.exists(path):
        #
        #         os.makedirs(path)
        #
        #     if self.save_pic(url,name):
        #
        #         return os.path.abspath(f"./data/daily_math/{name}"),list_name

    def save_pic (self,url,name) -> bool:

        if url:
            res = requests.get(url)
            len_res = len(res.content)
            # path: Path = Path().absolute() / rf".\data\daily_math\{name}"
            name = name.replace("/"," ")
            path: str = os.path.abspath(f"./data/daily_math/{name}")
            try:
                with open(path, 'wb') as f:
                    f.write(res.content)
                return True
            except OSError as oos:
                pass
            except Exception as e:
                raise e
                return False
        return False

    def save_precise_pic(self, url, name):
        res = requests.get(url)
        today_pic: str = re.findall(r"(今日习题.*?)(data-src=\")(.*?)\"", res.text)[0][2]
        return self.save_pic(today_pic, name)
        

    def get_weekpra(self):

        self.url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzk0NjA5MjEzNQ==&action=getalbum&album_id=2895437849775308801&scene=173&from_msgid=2247515620&from_itemidx=1&count=3&nolastread=1#wechat_redirect"
        res = requests.get(self.url)
        url_list: list[tuple[str]] = re.findall('(url: \')(.*)(\')',res.text) # 元祖列表
        name_list = re.findall('(title: \')(.*?)(\')',res.text)
        for index, tu in enumerate(url_list):
            if url_list:
                try:
                    if "解析" not in name_list[index] and self.record_download(name_list[index][1]):
                        url = tu[1].replace('amp;', "")
                        res = requests.get(url)
                        url = re.search("(.*周周清.*)(data-src=\")(.*?)(\".*?关于答案)", res.text)
                        pic_url = url.groups()[2]
                        res = requests.get(pic_url).content
                        with open("./data/daily_math/" + name_list[index][1] + ".png", 'wb') as f:
                            f.write(res)
                        return "./data/daily_math/" + name_list[index][1] + ".png"
                except Exception as e:
                    raise e
                    return ""
            else:
                return ""

    def record_download (self,name: str) -> bool:

        path = "./data/daily_math/exist"
        list_download = []
        if not os.path.exists(path):
            os.makedirs(path)
        try:
            with open(path+"/exist.json", 'r') as f:
                content = json.load(f)
                list_download = content['list_download']
        except FileNotFoundError:
            pass
        except Exception:
            pass
        if name in list_download:
            return False

        with open(path+"/exist.json", 'w',encoding='utf-8') as f:
            if name not in list_download or list_download:
                list_download.append(name)
                json.dump({'list_download':list_download},f,indent=4)
        return True

    def write(self,math: daily_math):

        path = "./data/daily_math/content"

        if not os.path.exists(path):
            os.makedirs(path)

        list_content: list = self.read()

        if math.__dict__() not in list_content:
            list_content.append(math.__dict__())

        with open(path+"/content.json", 'w', encoding='utf-8')as f:
            json.dump(list_content,f,ensure_ascii=False)


    def read(self) -> list[dict]:

        path = "./data/daily_math/content"
        try:
            with open(path + "/content.json", 'r', encoding='utf-8') as f:
                list_content = list(json.load(f))
        except Exception as e:
            return []
        return list_content


if __name__ == '__main__':
    wb = WebSpider()
    wb.parse_loop()
