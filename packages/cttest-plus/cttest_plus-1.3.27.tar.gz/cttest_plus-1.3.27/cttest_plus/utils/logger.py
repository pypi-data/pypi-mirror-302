import logging
from loguru import logger

from cttest_plus.globalSetting import plus_setting


class PlusHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


logger.add(PlusHandler(), format="{time:YYYY-MM-DD HH:mm:ss} | {message}", level=plus_setting.LEVEL)
