# coding:utf-8

import random

import nonebot
from nonebot import logger
import functools

from .models import *
from .config import NoUserInfoException


def check_coins_required(coins_required: int):
    '''params: coins_required: 需要的 coin 数量
        其中 bot, user_id, group_id 为关键字参数
        必须写在调用函数中
    '''

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # 获取机器人实例
                bot = kwargs['bot']
                # 获取用户的 QQ 号
                user_id = kwargs['user_id']
                # 获取群号
                group_id = kwargs['group_id']
            except Exception:
                logger.error(f"调用函数中缺少bot, user_id, group_id参数")
                return

            # 查询用户的 coin 数量
            coins = await get_user_coins(user_id=user_id, group_id=group_id)
            nickname = await get_user_nickname(user_id=user_id, group_id=group_id)
            if coins == -1:
                await bot.send_group_msg(
                    group_id=group_id,
                    message=f"用户不存在\n请先注册!(使用register命令)"
                )
                logger.error(f"{user_id} 不存在")
                raise NoUserInfoException("用户不存在")

            if coins >= coins_required:

                # 调用原始函数
                await func(*args, **kwargs)

                # 扣除相应的 coin
                await reduce_user_coins(user_id=user_id,
                                        group_id=group_id,
                                        coins_to_reduce=coins_required)

                await bot.send_group_msg(
                    group_id=group_id,
                    message=f"{nickname}使用了{coins_required}个coin!"
                )

            else:
                # 给出提示

                await bot.send_group_msg(
                    group_id=group_id,
                    message=f"{nickname}的 coin 不足，需要 {coins_required} 个 coin!"
                )
                logger.error(f"{user_id} 的 coin 不足，需要 {coins_required} 个 coin!")
                return

        return wrapper

    return decorator


def add_coin_after_call(coins_to_add: int = random.randint(20,40)):
    '''
    params: coins_to_add: 需要增加的 coin 数量
    其中 user_id, group_id, bot 为关键字参数
    必须写在调用函数中
    '''

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # 获取用户的 QQ 号
                nonebot.logger.info(kwargs)
                user_id = kwargs['user_id']
                # 获取群号
                group_id = kwargs['group_id']
                # 获取bot实例
                bot = kwargs['bot']
            except Exception:
                logger.error(f"调用函数中缺少user_id, group_id参数")
                raise Exception
                # 查询用户的 coin 数量
            coins = await get_user_coins(user_id=user_id, group_id=group_id)
            if coins == -1:
                logger.error(f"用户 {user_id} 不存在")
                raise NoUserInfoException

            # 调用原始函数
            res = await func(*args, **kwargs)

            # 增加用户的 coin 数量并保存更改

            if not await add_user_coins(user_id=user_id, group_id=group_id, coins_to_add=coins_to_add):
                nickname = await get_user_nickname(user_id, group_id)
                bot.send_group_msg(group_id=group_id, message=f'{nickname}成功获得{coins_to_add}个coin!')

            return res

        return wrapper

    return decorator


async def add_coin_to_all_users(coin_to_add: int):
    '''
    params: coin_to_add: 需要增加的 coin 数量
    为数据库中所有存在的用户增加 coin
    '''
    list_user = get_all_users()

    for user in list_user:
        user_id = user.user_id
        group_id = user.group_id
        await add_user_coins(user_id=user_id, group_id=group_id, coins_to_add=coin_to_add)


if __name__ == '__main__':
    asyncio.run(init_db())
    asyncio.run(close_db())
