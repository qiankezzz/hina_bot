import requests
from bs4 import BeautifulSoup

id = 2247508513
id_list = []
while 1:
    try:
        url = f"https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz=Mzk0NjA5MjEzNQ==&album_id=2644861174949462016&count=10&begin_msgid={id}&begin_itemidx=2&uin=&key=&pass_ticket=&wxtoken=&devicetype=&clientversion=&__biz=Mzk0NjA5MjEzNQ==&appmsg_token=&x5=0&f=json"
        id += 1
        res = requests.get(url).json()["getalbum_resp"]['article_list']
        print(id-1)
        print(url)
        id_list.append(id-1)
        for ittm in res:
            print(ittm['title'])
            print(ittm['url'])
        if '180' in ittm['title']:
            break

    except:
        pass

print(id_list)
