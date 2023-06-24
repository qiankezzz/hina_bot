from nonebot import get_driver, on_command, on_keyword, on_fullmatch, on_notice
from nonebot.adapters.onebot.v11 import Event, Message, MessageSegment
from .config import Config



global_config = get_driver().config
config = Config.parse_obj(global_config)

update_name = on_notice()

private_command = on_command("私聊命令",priority=4)
group_command = on_command("群聊命令",priority=4)

hina = on_keyword({"日菜",'hina','Hina'},priority=10)

menu = on_fullmatch("菜单",priority=4)
hao = on_fullmatch("好",priority=3)
wuyu = on_fullmatch("无语了",priority=4)
wokao = on_fullmatch("我靠",priority=4)



@update_name.handle()
async def _(event: Event):
    if notice_group_card := event.get_event_description():
        notice_dict = eval(notice_group_card)
        if notice_dict['notice_type'] == 'group_card':
            card_old, card_new, user_id = notice_dict['card_old'], notice_dict['card_new'], notice_dict['user_id']
            await update_name.finish(Message(f"[CQ:at,qq={user_id}]的状态由{card_old}转变为{card_new}了哦~"))





@menu.handle()
async def _() -> None:
    menu_str : str= "有什么想问小日菜的吗~\n私聊命令|群聊命令"
    await menu.finish(Message(menu_str))


@group_command.handle()
async def _() -> None:

    command_str : str = "早安/:早上好哦~\n晚安:晚安喽~\n抽签:签到--噜♪的一天的开始喽~(今日运势帮助可查看规则~)\n" \
                        "awsl(+次数):奖励~\nchat:和New Bing对话吧~\n"\
                        "召唤/戳:日菜会代替召唤你要找的人哦~(设置召唤+@+名字可以进行设置哦)\n撤回:撤回日菜的消息~\n" \
                        "inform+name:停止/开启提醒~\n每日一题:查看每日一题目录~\ncheck:查看每日一题的题目~\ncos:随机抽取米游社的一张" \
                        "图~\ngpt:和GPT3.5对话吧~\nopen:开箱~(cases,svs查看箱子名称)\n日菜还会持续更新的哦~"

    await group_command.finish(Message(command_str))

@private_command.handle()
async def _() -> None:
    pass

@wuyu.handle()
async def _() -> None:
    
    await wuyu.finish(MessageSegment.image(file='file:///C:\\hina bot\\hinabot2\\data\\mazui_study/wuyu.jpg'))


@hao.handle()
async def _() -> None:
    
    await hao.finish(MessageSegment.image(file='file:///C:\\hina bot\\hinabot2\\data\\mazui_study/hao.png'))

    
@wokao.handle()
async def _() -> None:
    
    await wokao.finish(MessageSegment.image(file='file:///C:\\hina bot\\hinabot2\\data\\mazui_study/kao.png'))

'''
↓需要修改添加↓
'''

@hina.handle()
async def _() -> None:
    
    await hina.finish(Message("叫日菜什么事啊~"))

