import os
from argparse import Namespace
import uuid
import time

import pytest
from json_verify import JsonVerify

from cttest_plus.globalSetting import plus_setting
from cttest_plus.utils.logger import logger
from cttest_plus.utils.download import build_file
from cttest_plus.drivers.driverBy import DriverBy
from cttest_plus.globalSetting import DYNAMIC_FILE, DYNAMIC_SETTING_FILE, DYNAMIC_VERIFY_FIlE
from cttest_plus.utils.initTest import _Config, RunningSummery
from cttest_plus import globalSetting


class TestFactory:
    uuid = uuid.uuid1()
    @classmethod
    def run(cls, command_args=None, runner_name="pytest", kwargs=Namespace(), build=True):
        """
        测试执行入口
        :param command_args: 远程主机发送经过ShellParams类
        :return: None

        """
        try:
            _Config.load_func()
            if build:
                logger.info(f"【用例文件】下载中····")
                build_file(kwargs.url, DYNAMIC_FILE)
                logger.info(f"【配置文件】下载中····")
                build_file(kwargs.config, DYNAMIC_SETTING_FILE)
                logger.info(f"【契约文件】下载中····")
                if kwargs.verify:
                    build_file(kwargs.verify, DYNAMIC_VERIFY_FIlE)

            if command_args is None: command_args = []

            runner = getattr(cls, f"_{runner_name}")
            runner(command_args)

        finally:
            for driver_name, driver_class in DriverBy.__dict__.items():
                if not isinstance(driver_class, str) and hasattr(driver_class, "session_class"):
                    driver_class.session_class.close()
            dynamic_test_file = plus_setting.BASE_DIR+"/test_case/"+DYNAMIC_FILE
            dynamic_config = plus_setting.BASE_DIR+"/test_case/"+DYNAMIC_SETTING_FILE
            dynamic_verify = plus_setting.BASE_DIR+"/test_case/"+DYNAMIC_VERIFY_FIlE
            print(dynamic_test_file)
            if os.path.exists(dynamic_test_file):
                logger.info(f"正在删除动态文件")
                os.remove(dynamic_test_file)
                os.remove(dynamic_config)
                os.remove(dynamic_verify)
            else:
                logger.info(f"动态文件不存在")
            wait_time = globalSetting.WAIT_TIME_COUNT
            logger.info(f"测试计划执行过程中，等待耗时 {wait_time//60}m {wait_time%60}s")
            if RunningSummery.video_info and len(RunningSummery.run_record)>1:
                logger.info(f'【视频等待】等待视频生成···')
                time.sleep(5)
                video_path = os.path.dirname(plus_setting.BASE_DIR) + '/videos'
                RunningSummery(video_path).clip_video()

    @classmethod
    def _pytest(cls, command):
        command.append(plus_setting.BASE_DIR + r'/test_case')
        command += ["-s", "-p", "cttest_plus.core.pytestLoader", '-p','no:warnings', '--show-capture=no']
        pytest.main(command)

    @classmethod
    def _unittest(cls, command, *args):
        raise ValueError(f'【执行器错误】暂不支持{cls.__class__.__name__}执行器')

    @classmethod
    def _behavior(cls, command, *args):
        raise ValueError(f'【执行器错误】暂不支持{cls.__class__.__name__}执行器')
