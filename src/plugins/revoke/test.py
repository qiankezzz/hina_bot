import re
str1 = "[CQ:reply,id=-621339101][CQ:at,qq=2293348860] /撤回"
# 获取id=后面的数字
message_id = re.findall(r'\[CQ:reply,id=(-?\d+)\]', str1)
print(message_id)