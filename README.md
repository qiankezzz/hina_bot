# hina_bot
****
基于 Nonebot2 和 go-cqhttp 开发的QQ群娱乐机器人

  
## 关于

作为大一python课设提交的QQ机器人，某些功能学习借鉴了大佬们的代码，

日菜bot，实现了一些对群友的娱乐功能和实用功能（大概）。

<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">


  
# NoneBot

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_✨ 跨平台 Python 异步机器人框架 ✨_
<!-- prettier-ignore-end -->
  
非常 [ **[NICE](https://github.com/nonebot/nonebot2)** ] 的OneBot框架
  
</div>

# 简单部署

```

# 配置gocq

在 https://github.com/Mrs4s/go-cqhttp 下载Releases最新版本，运行后选择反向代理，
  后将gocq的配置文件config.yml中的universal改为universal: ws://127.0.0.1:8080/onebot/v11/ws

gocq配置详情稍后补充

# 获取代码
git clone https://github.com/qiankezzz/hina_bot.git

# 进入目录
cd hina_bot

# 开始运行
python bot.py
```

## 功能列表

<details>
<summary>已实现的功能</summary>

### 可以使用群聊命令/私聊命令获取指令~

### 已实现的常用功能

* [x] 昵称系统（群与群与私聊分开.）
* [x] [让Bot学习群友说话和发表情包！](https://github.com/CMHopeSunshine/nonebot-plugin-learning-chat)
* [x] 让Bot发送一定数量图片~(存在CD)
* [x] [在群内监控播报群友的Steam游戏状态](https://github.com/nek0us/nonebot_plugin_steam_game_status)
* [x] 获取武宗祥老师的考研数学每日一练~ 
* [x] [使用新版必应的聊天功能](https://github.com/Harry-Jing/nonebot-plugin-bing-chat)
* [x] 主动撤回Bot的不当话语~
* [x] [抽签！抽取你的今日运势🙏](https://github.com/MinatoAquaCrews/nonebot_plugin_fortune)
* [x] 获取米游社原神cos图片~
* [x] [早晚安记录作息，培养优质睡眠😴](https://github.com/MinatoAquaCrews/nonebot_plugin_morning) 
* [x] 定时提醒群友学习，根据学习状态发送特定内容~
* [x] [模拟csgo开箱](https://github.com/roiiiu/nonebot-plugin-csgo-case-simulator)

</details>



## 感谢

[botuniverse / onebot](https://github.com/botuniverse/onebot) ：超棒的机器人协议  
[Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp) ：cqhttp的golang实现，轻量、原生跨平台.  
[nonebot / nonebot2](https://github.com/nonebot/nonebot2) ：跨平台Python异步机器人框架  
