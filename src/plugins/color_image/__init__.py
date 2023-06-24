from nonebot import get_driver, on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent, Message, MessageSegment
from pathlib import Path
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg, ArgPlainText

import nonebot

from .config import Config
from .utils import *
from ..coin_system.utils import check_coins_required

global_config = get_driver().config
config = Config.parse_obj(global_config)

setu = on_command('awsl', aliases={'awsl'}, block=True, priority=5)
setu_class = on_command('awslclass', aliases={'awsl_class'}, block=True, priority=5)

@setu.handle()
async def _(event: Event,
            matcher : Matcher,
            args : Message = CommandArg()):

    num = args.extract_plain_text()
    if num:
        matcher.set_arg("num",args)

class_dict = {
        '随机':'random',
        '壁纸推荐':'top',
        '银发':'yin',
        '兽耳':'cat',
        '星空':'xing',
        '竖屏壁纸':'mp',
        '横屏壁纸':'pc'
    }


@setu.got("num",prompt="想要日菜发多少张图呢~")
async def _(bot: Bot, event: MessageEvent, num_name: str = ArgPlainText("num")):
    num_name, type = extract_args(num_name)
    # color图片缓存路径
    t1 = os.path.abspath("./data/color_image/")
    color_cq : str = 'file:///'+ t1
    message_type = event.dict()['message_type']
    group_id = ""
    if message_type == "group":
        group_id = event.dict()['group_id']
    user_id = event.get_user_id()

    @check_coins_required(num_name)
    async def send_setu(**kwargs):

        if num_name <= 10:

            if await read_date():

                id_params = await setu.send(Message("小日菜正在处理哦~"))
                message_id = id_params['message_id']

                # 缓存color图片
                await load_pic(num_name, class_dict[type])
                # 写入CD
                await write_date()
                # 发送
                if message_id:
                    await bot.delete_msg(message_id=message_id)
                try:
                    await send_group_forward_msg(bot, group_id, user_id, num_name)
                except Exception as e:
                    nonebot.logger.error(e)
                    await setu.send(Message("图片可能过界了哦~"))
                    raise e

                await setu.send(Message(f"一共{num_name}张图哦~"))

            else:
                # CD未冷却
                await setu.finish(Message("小日菜还没准备好哦~"))

    await send_setu(bot=bot, group_id=group_id, user_id=user_id)


@setu_class.handle()
async def _():
    tstr = ""
    for index, key in enumerate(class_dict.keys()):
        if key == "随机":
            key = key + "(默认)"
        tstr = tstr + index + "." + key + '\n'
    await setu_class.finish(tstr)


def extract_args(args: str):
    arg_list = args.split(" ")
    if len(arg_list) > 0 and arg_list[0] != "":
        if len(arg_list) == 2:
            num = int(arg_list[0])
            num = num if num < 10 else 10
            type = arg_list[1]
        else:
            num = int(arg_list[0])
            num = num if num < 10 else 10
            type = "随机"
        return num, type
    else:
        return 1, "随机"





async def send_group_forward_msg(bot: Bot, group_id: int,user_id: int, num: int = 0):
    # 构造消息段列表
    message_segments = []

    IMAGE_PATH = os.path.abspath("./data/color_image/")
    color_cq: str = f'file:///{IMAGE_PATH}'
    def to_json(msg):
        return {"type": "node", "data": {"name": 'hina', "uin": 2293348860, "content": msg}}


    for i in range(num):
        message_segments.append(MessageSegment.image(file=f'{color_cq}\{i}.png'))

    messages = [to_json(msg) for msg in message_segments]
    # 发送合并转发消息
    if group_id:
        await bot.send_group_forward_msg(
            group_id=group_id,
            messages=messages
        )
    else:
        await bot.send_private_forward_msg(
            user_id=user_id,
            messages=messages
        )