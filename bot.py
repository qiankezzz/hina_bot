import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

nonebot.init(apscheduler_autostart=True, apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

nonebot.load_builtin_plugins('echo', 'MyAPI', 'mazui_study', 'genshin_cos','daily_math')

nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()
