from pydantic import BaseModel, Extra

from nonebot import get_driver, logger

driver = get_driver()


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""


class NoUserInfoException(Exception):
    def __init__(self, message):
        self.message = message

    
    def __str__(self):
        return self.message

def log_debug(command: str, info: str):
    logger.opt(colors=True).debug(f'<u><y>[{command}]</y></u>{info}')


def log_info(command: str, info: str):
    logger.opt(colors=True).info(f'<u><y>[{command}]</y></u>{info}')
