import json

from cttest_plus.utils.logger import logger
from cttest_plus.utils.dataParser import JsonParser
from cttest_plus.utils.initTest import _Config
from cttest_plus.globalSetting import plus_setting

class CompatWEBDriver:
    driver = None
    video_url = None

    @classmethod
    def run(cls, *args, **kwargs):
        if cls.driver:
            cls.driver.quit()
        if cls.video_url:
            logger.info(f"【视频地址】{cls.video_url}")


class CompatAPPDriver:
    driver = None
    # video_url = None

    @classmethod
    def run(cls, *args, **kwargs):
        if cls.driver:
            cls.driver.quit()
        # if cls.video_url:
            # logger.info(f"【视频地址】{cls.video_url}")


class SetVariable:
    @classmethod
    def run(cls, data_set, uuid=None, owner_var_map=None, *args, **kwargs):
        if not _Config.environment:
            with open(plus_setting.BASE_DIR + '/test_case/projectSetting.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            _Config.set_config(config)
            _Config.load_func()
        param = data_set.get("request").get("test_data")
        param = JsonParser.analyze(param, uuid=uuid, owner_var_map=owner_var_map)
        JsonParser.add_variable(param, uuid=uuid)


# class SysDatabase:
#     @classmethod
#     def run(cls):