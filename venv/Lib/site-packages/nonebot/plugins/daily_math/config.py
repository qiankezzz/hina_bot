# coding:utf-8
from pydantic import BaseModel,Extra,BaseSettings,Field


class time(BaseSettings):
    hour: int = Field(0,alias='HOUR')
    minute: int = Field(0,alias='MINUTE')

    class Config:
        extra = "allow"
        case_sensitive = False
        anystr_lower = True

class Config(BaseSettings):
    daily_group_id: list[int] = []
    daily_send_time: list[time] = []

    class Config:
        extra = Extra.allow
        case_sensitive = False