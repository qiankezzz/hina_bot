import nonebot
from nonebot import on_command, on_regex, on_fullmatch
from nonebot.log import logger
from nonebot.plugin import PluginMetadata
from nonebot.params import Depends, CommandArg, RegexMatched
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot import require
from nonebot.adapters.onebot.v11 import GROUP, GROUP_ADMIN, GROUP_OWNER, Message, GroupMessageEvent, MessageSegment
from .data_source import fortune_manager
from .config import FortuneThemesDict

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from ..coin_system.utils import add_coin_after_call

__fortune_version__ = "v0.4.10.post1"
__fortune_usages__ = f'''
[今日运势/抽签/运势] 一般抽签
[xx抽签]     指定主题抽签
[指定xx签] 指定特殊角色签底，需要自己尝试哦~
[设置xx签] 设置群抽签主题
[重置主题] 重置群抽签主题
[主题列表] 查看可选的抽签主题
[查看主题] 查看群抽签主题'''.strip()

__plugin_meta__ = PluginMetadata(
    name="今日运势",
    description="抽签！占卜你的今日运势🙏",
    usage=__fortune_usages__,
    extra={
        "author": "KafCoppelia <k740677208@gmail.com>",
        "version": __fortune_version__
    }
)

general_divine = on_command("今日运势", aliases={"抽签", "运势"}, permission=GROUP, priority=8)
specific_divine = on_regex(r"^[^/]\S+抽签$", permission=GROUP, priority=8)
limit_setting = on_regex(r"^指定(.*?)签$", permission=GROUP, priority=8)
change_theme = on_regex(r"^设置(.*?)签$", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=8, block=True)
reset_themes = on_regex("^重置(抽签)?主题$", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=8, block=True)
themes_list = on_fullmatch("主题列表", permission=GROUP, priority=8, block=True)
show_themes = on_regex("^查看(抽签)?主题$", permission=GROUP, priority=8, block=True)


@show_themes.handle()
async def _(event: GroupMessageEvent):
    gid: str = str(event.group_id)
    theme: str = fortune_manager.get_group_theme(gid)
    await show_themes.finish(f"当前群抽签主题：{FortuneThemesDict[theme][0]}")


@themes_list.handle()
async def _(event: GroupMessageEvent):
    msg: str = fortune_manager.get_available_themes()
    await themes_list.finish(msg)


@general_divine.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    arg: str = args.extract_plain_text()

    if "帮助" in arg[-2:]:
        await general_divine.finish(__fortune_usages__)

    gid: str = str(event.group_id)
    uid: str = str(event.user_id)

    is_first, image_file = fortune_manager.divine(gid, uid, None, None)
    if image_file is None:
        await general_divine.finish("今日运势生成出错……")

    if not is_first:
        msg = MessageSegment.text("你今天抽过签了，再给你看一次哦🤗\n") + MessageSegment.image(image_file)
    else:
        logger.info(f"User {uid} | Group {gid} 占卜了今日运势")

        bot = nonebot.get_bot()

        @add_coin_after_call()
        async def temp(**kwargs):
            return MessageSegment.text("✨今日运势✨\n") + MessageSegment.image(image_file)

        msg = await temp(user_id=uid, group_id=gid, bot=bot)

    await general_divine.send(msg, at_sender=True)


async def get_user_theme(matcher: Matcher, args: str = RegexMatched()) -> str:
    arg: str = args[:-2]
    if len(arg) < 1:
        await matcher.finish("输入参数错误")

    return arg


@specific_divine.handle()
async def _(event: GroupMessageEvent, user_theme: str = Depends(get_user_theme)):
    for theme in FortuneThemesDict:
        if user_theme in FortuneThemesDict[theme]:
            if not fortune_manager.theme_enable_check(theme):
                await specific_divine.finish("该抽签主题未启用~")
            else:
                gid: str = str(event.group_id)
                uid: str = str(event.user_id)

                is_first, image_file = fortune_manager.divine(
                    gid, uid, theme, None)
                if image_file is None:
                    await specific_divine.finish("今日运势生成出错……")

                if not is_first:
                    msg = MessageSegment.text("你今天抽过签了，再给你看一次哦🤗\n") + MessageSegment.image(image_file)
                else:
                    logger.info(f"User {uid} | Group {gid} 占卜了今日运势")
                    msg = MessageSegment.text("✨今日运势✨\n") + MessageSegment.image(image_file)

            await specific_divine.finish(msg, at_sender=True)

    await specific_divine.finish("还没有这种抽签主题哦~")


async def get_user_arg(matcher: Matcher, args: str = RegexMatched()) -> str:
    arg: str = args[2:-1]
    if len(arg) < 1:
        await matcher.finish("输入参数错误")

    return arg


@change_theme.handle()
async def _(event: GroupMessageEvent, user_theme: str = Depends(get_user_arg)):
    gid: str = str(event.group_id)

    for theme in FortuneThemesDict:
        if user_theme in FortuneThemesDict[theme]:
            if not fortune_manager.divination_setting(theme, gid):
                await change_theme.finish("该抽签主题未启用~")
            else:
                await change_theme.finish("已设置当前群抽签主题~")

    await change_theme.finish("还没有这种抽签主题哦~")


@limit_setting.handle()
async def _(event: GroupMessageEvent, limit: str = Depends(get_user_arg)):
    logger.warning("指定签底抽签功能将在 v0.5.x 弃用")

    gid: str = str(event.group_id)
    uid: str = str(event.user_id)

    if limit == "随机":
        is_first, image_file = fortune_manager.divine(gid, uid, None, None)
        if image_file is None:
            await limit_setting.finish("今日运势生成出错……")
    else:
        spec_path = fortune_manager.specific_check(limit)
        if not spec_path:
            await limit_setting.finish("还不可以指定这种签哦，请确认该签底对应主题开启或图片路径存在~")
        else:
            is_first, image_file = fortune_manager.divine(gid, uid, None, spec_path)
            if image_file is None:
                await limit_setting.finish("今日运势生成出错……")

    if not is_first:
        msg = MessageSegment.text("你今天抽过签了，再给你看一次哦🤗\n") + MessageSegment.image(image_file)
    else:
        logger.info(f"User {uid} | Group {gid} 占卜了今日运势")
        msg = MessageSegment.text("✨今日运势✨\n") + MessageSegment.image(image_file)

    await limit_setting.finish(msg, at_sender=True)


@reset_themes.handle()
async def _(event: GroupMessageEvent):
    gid: str = str(event.group_id)
    if not fortune_manager.divination_setting("random", gid):
        await reset_themes.finish("重置群抽签主题失败！")

    await reset_themes.finish("已重置当前群抽签主题为随机~")


# 清空昨日生成的图片
@scheduler.scheduled_job("cron", hour=0, minute=0, misfire_grace_time=60)
async def _():
    fortune_manager.clean_out_pics()
    logger.info("昨日运势图片已清空！")
