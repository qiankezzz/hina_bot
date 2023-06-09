from nonebot import on_command, require
from nonebot.params import MessageSegment
import os, requests

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Message, MessageEvent
from nonebot.params import CommandArg, ArgPlainText, Arg
from nonebot.matcher import Matcher
import nonebot
from .utils import WebSpider, daily_math
from .config import Config

# 配置信息
global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

# 检测是否存在配置信息
if hasattr(plugin_config, 'daily_group_id') and hasattr(plugin_config, 'daily_send_time'):
    pass
    # nonebot.logger.success("plugin_config:{}".format(plugin_config))
else:
    # nonebot.logger.critical("plugin_config:{}".format(plugin_config))
    raise Exception("daily_math config error, please check env file")

# 注册响应器
daily_math_ = on_command("每日一题", priority=4)
daily_math_check = on_command("check", priority=4)
daily_math_init = on_command("checkinit", priority=4)

'''
存在目录
使得输入一题发送一题
'''


@daily_math_init.handle()
async def _():
    wb = WebSpider()
    wb.parse_loop()
    await daily_math_init.finish("初始化完成!")


@daily_math_.handle()
async def _(bot: Bot, event: MessageEvent):
    wb = WebSpider()
    temp_str = ""
    list_content = []
    message_type = event.dict()['message_type']

    def to_json(msg):
        return {"type": "node", "data": {"name": 'hina', "uin": 2293348860, "content": msg}}

    for title, url in zip(wb.parse()[3], wb.parse()[2]):
        url = url.replace("amp;", "")
        temp_str = title + "\n" + url
        list_content.append(temp_str)

    messages = [to_json(msg) for msg in list_content]

    if message_type == "group":
        group_id = event.dict()['group_id']
        await bot.send_group_forward_msg(
            messages=messages,
            group_id=group_id
        )
    else:
        user_id = event.get_user_id
        await bot.send_private_forward_msg(
            messages=messages,
            user_id=user_id
        )


# 查看指定题目
@daily_math_check.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    if title := args.extract_plain_text():
        matcher.set_arg("title", args)


@daily_math_check.got("title", prompt="想看哪一题呢~")
async def _(title: str = ArgPlainText()):
    wb = WebSpider()
    name = ""
    url = ""
    for index, math in enumerate(wb.read()):
        o_title = math['title']
        if title in o_title:
            name = o_title
            url = math['url']
            break

    try:
        if name:
            path = "file:///" + os.path.abspath(f"./data/daily_math/{name}.png")
            if os.path.exists(path):
                await daily_math_check.send(Message(f'好的噜~\n{name}') + MessageSegment.image(file=path))
            elif wb.save_precise_pic(url, name + ".png"):
                await daily_math_check.send(Message(f'好的噜~\n{name}') + MessageSegment.image(file=path))
            else:
                await daily_math_check.finish("查询时出现错误~")
            await daily_math_check.send(Message(f"答案请去此处查询哦~\n{url}"))
        else:
            await daily_math_check.send(Message("暂时无法查询该题目哦~(可尝试输入checkinit解决哦~)"))
    except Exception as e:
        await daily_math_check.send("查询时出现错误~")

    pass


# 定时提醒
@scheduler.scheduled_job("cron", hour=12, minute=30, id="114514")
async def _():
    bot = nonebot.get_bot()
    wb = WebSpider()
    path, name, path_extra, url = wb.save_all_pic()[0], wb.save_all_pic()[1], wb.save_all_pic()[2], wb.save_all_pic()[3]
    wb.write(daily_math(name, url))

    for group_id in plugin_config.daily_group_id:

        if path:
            await bot.send_group_msg(
                message=Message(f"今日的午练是~\n{name}") + MessageSegment.image(file="file:///" + path),
                group_id=group_id
            )
        if path_extra:
            await bot.send_group_msg(
                message=Message(f"知识补充~" + MessageSegment.image(file="file:///" + path_extra)),
                group_id=group_id
            )
