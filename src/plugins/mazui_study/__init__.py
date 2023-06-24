# coding:utf-8

'''
以下为定时任务插件:
apscheduler_autostart = "True"  # 是否自动启动 APScheduler
apscheduler_config = {"apscheduler.timezone": "Asia/Shanghai"} # APScheduler 相关配置。
'''

import os
import datetime
import json
import random

import nonebot
from nonebot.matcher import Matcher
from nonebot import on_message, require, on_command
from nonebot.adapters import Message, Bot, Event
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters.onebot.v11 import GROUP
from .config import Config
from .utils import utils

# 获取信息
mazui = on_message(priority=99, block=False, permission=GROUP)
open = on_command("inform", priority=5, permission=GROUP)

global_config = nonebot.get_driver().config
# nonebot.logger.info("global_config:{}".format(global_config))
plugin_config = Config(**global_config.dict())

'''
Need info:
uid : list : ?
group_id : list : ?
inform_time : list[dict] : ?
'''

# 检测是否存在配置信息
if hasattr(plugin_config, 'group_id') and hasattr(plugin_config, 'uid'):
    pass
    # nonebot.logger.success("plugin_config:{}".format(plugin_config))
else:
    # nonebot.logger.critical("plugin_config:{}".format(plugin_config))
    raise Exception("mazui_study config error, please check env file")


@mazui.handle()
async def _(event: Event):
    state = utils.read_study('mazui_state')

    if event.get_user_id() == "983853001" and not state:
        mazui_params: json = utils.mod_json_data('mazui_state', True)  # 马嘴开始学习
        utils.write_study(mazui_params)
    # 发疯人格    
    elif event.get_user_id() == "3403093523":
        zxh_params_1: json = utils.mod_json_data('zxh_state', True)  # True 代表发疯
        utils.write_study(zxh_params_1)
    # 正常人格
    elif event.get_user_id() == "2864818644":
        zxh_params_2: json = utils.mod_json_data('zxh_state', False)  # False 代表正常
        utils.write_study(zxh_params_2)
        state = utils.read_study('zxh_state_study')
        if not state:
            params: json = utils.mod_json_data_dict({'zxh_state_studying': False, 'zxh_state_study': True})  # zxh出现
            utils.write_study(params)


@open.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    name: str = args.extract_plain_text()
    if name:
        matcher.set_arg("name", args)


@open.got("name", prompt="要调整谁的提醒呢~")
async def _(name_str: str = ArgPlainText("name")):
    state: bool = utils.read_study('inform_state_mazui')

    state_zxh: bool = utils.read_study('inform_state_zxh')

    if name_str == "马嘴":

        if state:
            await open.send("停止提醒马嘴了哦~")
            temp_params: json = utils.mod_json_data('inform_state_mazui', False)
            utils.write_study(temp_params)

        else:
            await open.send("开始提醒马嘴了哦~")
            temp_params: json = utils.mod_json_data('inform_state_mazui', True)
            utils.write_study(temp_params)

    elif name_str == "zxh":

        if state_zxh:
            await open.send("停止提醒zxh了哦~")
            temp_params: json = utils.mod_json_data('inform_state_zxh', False)
            utils.write_study(temp_params)

        else:
            await open.send("开始提醒zxh了哦~")
            temp_params: json = utils.mod_json_data('inform_state_zxh', True)
            utils.write_study(temp_params)

    else:
        await open.finish("ta还不需要日菜提醒哦~")


require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

path = os.path.abspath(os.path.dirname(__file__))


async def inform_sleep():
    arr = ['5.png', '6.jpg']
    message_sleep: str = f'日菜要去找欧内酱睡觉了哦(ゝω・´★)!~你也一起来吧♪[CQ:image,file=file:///{path}/data\mazui_study/' + '{0}]'.format(
        arr[random.randint(0, 1)])

    for qq_group in plugin_config.group_id:
        await nonebot.get_bot().send_group_msg(group_id=qq_group, message=message_sleep)


async def inform_eat():
    arr = ['4.png', '13.png']
    message_eat: str = f'日菜酱来叫你一起吃饭了哦~[CQ:image,file=file:///{path}\data\mazui_study/' + '{0}]'.format(
        arr[random.randint(0, 1)])

    for qq_group in plugin_config.group_id:
        await nonebot.get_bot().send_group_msg(group_id=qq_group, message=message_eat)


async def inform_zxh() -> None:
    message_study: str = "小日菜来叫[CQ:at,qq=2864818644]学习啦～\n再不学习就保不了研了"

    for qq_group in plugin_config.group_id:
        await nonebot.get_bot().send_group_msg(group_id=qq_group, message=message_study)


async def inform_mazui() -> None:
    arr = ['1.gif', '2.gif', '3.png', '9.png', '10.jpg']

    message_study_zxh: str = f'小日菜来叫[CQ:at,qq=2864818644]学习啦～\n再不学习就保不了研了哦~[CQ:image,file=file:///{path}\data\mazui_study/' + '{0}]'.format(
        arr[random.randint(0, len(arr) - 1)])

    # 暂时没想到
    message_studying_zxh: str = '[CQ:at,qq=2864818644]还在认真学习吗?\n那小日菜先不打扰了噜~还需要小日菜提醒要告诉我哦~' \
                                f'[CQ:image,file=file:///{path}\data\mazui_study/' + '{0}]'.format(
        ['11.jpg', ][0]
    )

    message_study: str = f'小日菜来叫[CQ:at,qq=983853001]学习啦~\n不学习可噜不起来哦...[CQ:image,file=file:///{path}/data\mazui_study/' + '{0}]'.format(
        arr[random.randint(0, len(arr) - 1)]
    )

    message_cry: str = f'[CQ:at,qq=983853001]不见了...\n是在休息还是在学习呢?[CQ:image,file=file:///{path}\data\mazui_study/14.jpg]'

    game_name: str = plugin_config.mazui_game[random.randint(0, len(plugin_config.mazui_game) - 1)]

    message_play: str = f'小日菜来叫[CQ:at,qq=983853001]打{game_name}啦~\n不打{game_name}可噜不起来哦!!!'

    for qq_group in plugin_config.group_id:

        state_mazui: bool = utils.read_study('mazui_state')
        state_zxh: bool = utils.read_study('zxh_state_study')
        week_day = datetime.datetime.now().weekday()

        open: bool = utils.read_study('inform_state_zxh')

        if open:
            if state_zxh:
                params = utils.mod_json_data('zxh_state_study', False)
                utils.write_study(params)
                await nonebot.get_bot().send_group_msg(group_id=qq_group, message=message_study_zxh)
            else:
                if not utils.read_study('zxh_state_studying'):
                    params = utils.mod_json_data('zxh_state_studying', True)
                    utils.write_study(params)
                    await nonebot.get_bot().send_group_msg(group_id=qq_group, message=message_studying_zxh)

        if week_day == 6 or week_day == 5:
            await nonebot.get_bot().send_group_msg(group_id=qq_group, message=message_play)
        else:
            open: bool = utils.read_study('inform_state_mazui')
            if open:
                if state_mazui:
                    params = utils.mod_json_data('mazui_state', False)
                    utils.write_study(params)
                    await nonebot.get_bot().send_group_msg(group_id=qq_group, message=message_study)
                else:
                    await nonebot.get_bot().send_group_msg(group_id=qq_group, message=message_cry)


# 遍历所有时间
for index, time in enumerate(plugin_config.inform_time):
    nonebot.logger.info("id:{},time:{}".format(index, time))
    if time.hour == 0:
        scheduler.add_job(inform_sleep, "cron", hour=time.hour, minute=time.minute, id=str(index))
    elif time.hour == 12 or time.hour == 18:
        scheduler.add_job(inform_eat, "cron", hour=time.hour, minute=time.minute, id=str(index))
    else:
        scheduler.add_job(inform_mazui, "cron", hour=time.hour, minute=time.minute, id=str(index))