import os
import time
from typing import Union
from common.lastb_entry import LastbEntry


class AppConfigError(Exception):
    pass


def _parse_bool(val: Union[str, bool]) -> bool:  # pylint: disable=E1136
    return val if type(val) == bool else val.lower() in ['true', 'yes', '1']


# AppConfig class with required fields, default values, type checking, and typecasting for int and bool values
class AppConfig:
    TRACE_LEVEL = os.getenv("APP_TRACE_LEVEL", "INFO")
    TOKEN = os.getenv("APP_TOKEN")
    MASTER_CHAT_ID = os.getenv("APP_MASTER_CHAT_ID")
    JOB_INTERVAL = int(os.getenv("APP_JOB_INTERVAL", "30"))
    OUTPUT_DELAY = int(os.getenv("APP_OUTPUT_DELAY", "5"))
    GLOBAL_STORED_ENTRY = LastbEntry(None, None, None)
    TS = time.time()

    def __init__(self, env):
        pass

    def __repr__(self):
        return str(self.__dict__)


# Expose Config object for app to import
Config = AppConfig(os.environ)


def get_config():
    return Config
