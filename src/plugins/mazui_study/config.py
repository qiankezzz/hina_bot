# coding:utf-8
import random
from pydantic import BaseModel,Extra,BaseSettings,Field

class time(BaseSettings):
    hour: int = Field(0,alias='HOUR')
    minute: int = Field(0,alias='MINUTE')

    class Config:
        extra = "allow"
        case_sensitive = False
        anystr_lower = True

class Config(BaseSettings):
    
    uid: list[int] = []
    group_id: list[int] = []
    inform_time: list[time()] = []
    mazui_game: list[str] = []

    class Config:
        extra = Extra.allow
        case_sensitive = False

    arr = ['1.gif', '2.gif', '3.png']
     
    params1 = {
        "message_type": 'group',
        "group_id": '1169648856',
        "message": '小日菜来叫[CQ:at,qq=983853001]学习啦~\n不学习可噜不起来哦...[CQ:image,file=file:///C:/Users/15368/PycharmProjects/pythonProject1/image/{0}]'.format(
            arr[random.randint(0, 2)])
    }
    params2 = {
        "message_type": 'group',
        "group_id": '1169648856',
        "message": '日菜酱来叫你一起吃饭了哦~[CQ:image,file=file:///C:/Users/15368/PycharmProjects/pythonProject1/image/4.png]'
    }
    params3 = {
        "message_type": 'group',
        "group_id": '1169648856',
        "message": '日菜要去找欧内酱睡觉了哦(ゝω・´★)!~你也一起来吧♪[CQ:image,file=file:///C:/Users/15368/PycharmProjects/pythonProject1/image/5.png]'
    }
    params5 = {
        "message_type": 'group',
        "group_id": '1169648856',
        "message": '小彩都生气了....\n[CQ:at,qq=983853001]还不学习....[CQ:image,file=file:///C:/Users/15368/PycharmProjects/pythonProject1/image/7.jpg]'
    }