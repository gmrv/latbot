import os
import time
from common.lastb_entry import LastbEntry


class AppConfig:
    TRACE_LEVEL = None
    TOKEN = None
    MASTER_CHAT_ID = None
    JOB_INTERVAL = None
    OUTPUT_DELAY = None
    GLOBAL_STORED_ENTRY = None
    APP_ABSOLUTE_PATH = None
    TS = None

    def __init__(self, env):
        self.TRACE_LEVEL = os.getenv("APP_TRACE_LEVEL", "INFO")
        self.TOKEN = os.getenv("APP_TOKEN")
        self.MASTER_CHAT_ID = os.getenv("APP_MASTER_CHAT_ID")
        self.JOB_INTERVAL = int(os.getenv("APP_JOB_INTERVAL", "30"))
        self.OUTPUT_DELAY = int(os.getenv("APP_OUTPUT_DELAY", "5"))
        self.GLOBAL_STORED_ENTRY = LastbEntry(None, None, None)
        self.TS = time.time()

    def __repr__(self):
        return str(self.__dict__)


# Expose Config object for app to import
Config = AppConfig(os.environ)


def get_config():
    return Config
