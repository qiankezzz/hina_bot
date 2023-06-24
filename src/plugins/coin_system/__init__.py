from pathlib import Path

import nonebot
from nonebot import get_driver, on_command, require
from nonebot.adapters.onebot.v11 import Event, GroupMessageEvent, Bot

from .utils import add_coin_to_all_users
from .config import Config
from .models import *

require('nonebot_plugin_apscheduler')
from nonebot_plugin_apscheduler import scheduler

global_config = get_driver().config
config = Config.parse_obj(global_config)

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").resolve())
)

register = on_command("register", block=True, priority=4)
check = on_command("checkcoin", block=True, priority=4)


@register.handle()
async def _(event: GroupMessageEvent):
    user_id = event.get_user_id()
    group_id = event.group_id
    nickname = event.sender.nickname
    async with database:
        exist = await add_user(user_id=user_id, group_id=group_id, nickname=nickname)
    if not exist:
        await register.finish(f"{nickname}注册成功!")
    else:
        await register.finish(f"{nickname}已经注册过了!")


@check.handle()
async def _(event: GroupMessageEvent):
    user_id = int(event.get_user_id())
    group_id = event.group_id

    async with database:
        coins = await get_user_coins(user_id=user_id, group_id=group_id)
        nickname = await get_user_nickname(user_id=user_id, group_id=group_id)
        if coins != -1:
            await check.finish(f"{nickname}的coin数量为{coins}!")
        else:
            await check.finish("用户不存在哦!请先注册(register)")


# 每日零点为数据库内的用户增加 20 个 coin
@scheduler.scheduled_job('cron', hour='0', minute='0', second='0')
async def _():
    async with database:
        await add_coin_to_all_users(20)
    bot = nonebot.get_bot()
    bot.logger.info('每日增加coin任务执行成功')
    group_id_list = await get_all_group_id()
    for group_id in group_id_list:
        await bot.send_group_msg(group_id=config.group_id, message='每日的coin刷新了哦~')
