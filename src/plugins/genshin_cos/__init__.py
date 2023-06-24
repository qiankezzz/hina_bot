# coding:utf-8
import nonebot
from nonebot import on_command
from .utils import WebSpider
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageSegment,Message,Bot, GroupMessageEvent
from nonebot.params import Arg,CommandArg,ArgPlainText,Event

req = on_command("cos",priority=5)
ws = utils.WebSpider()
gen = ws.save_pic()

@req.handle()
async def _(bot: Bot, event: Event, group_event: GroupMessageEvent):

    id_params = await req.send("小日菜正在处理哦~")
    message_id = id_params['message_id']

    group_id = group_event.group_id
    # group_id = event.get_session_id().split('_')[1]
    # ws = utils.WebSpider()
    # gen = ws.save_pic()
    global gen

    path : str = next(gen)
    print(path)
    
    if message_id:
        
        await bot.delete_msg(message_id=message_id)


    try:
        # id_params = await req.send(MessageSegment.image(file=path))
        id_params = await bot.send_group_msg(group_id=group_id, message=Message(f"[CQ:image,file=file:///{path}]"))
        message_id = id_params['message_id']
    except Exception:
        await req.send(Message("图片可以过界了哦~"))
        
        
@req.got("response",prompt="是否要再次发送一张呢?")
async def _(bot:Bot, event:Event, response:str = ArgPlainText()):
    if response == "是":
        id_params = await req.send("小日菜正在处理哦~")
        message_id = id_params['message_id']
        
        # ws = utils.WebSpider()
        # gen = ws.save_pic()
        global gen
        group_id = event.get_session_id().split('_')[1]

        path: str = next(gen)

        if message_id:
            await bot.delete_msg(message_id=message_id)

        try:
            id_params = await bot.send_group_msg(group_id=group_id,
                                                 message=Message(f"[CQ:image,file=file:///{path}]"))
            message_id = id_params['message_id']

        except Exception:
            await req.finish(Message("图片可能过界了哦~"))

        await req.reject("是否要再次发送一张呢?")
    else:
        await req.finish("结束了哦~")