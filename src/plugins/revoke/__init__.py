from nonebot import get_driver, on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent, Message, MessageSegment
from .config import Config

import re

global_config = get_driver().config
config = Config.parse_obj(global_config)


revoke = on_command("撤回", aliases={"撤回"}, block=True, priority=5)


@revoke.handle()
async def _(bot: Bot, event: MessageEvent):
    message = event.raw_message
    print(message)
    if 'reply' in message:
        message_id = int(re.findall(r'\[CQ:reply,id=(-?\d+)\]', message)[0])
        await bot.delete_msg(message_id=message_id)


