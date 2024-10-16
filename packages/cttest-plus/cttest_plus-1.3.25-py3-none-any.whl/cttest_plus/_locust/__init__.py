import sys
import time

if "ctlocust" in sys.argv[1]:
    try:
        # monkey patch all at beginning to avoid RecursionError when running locust.
        # `from gevent import monkey; monkey.patch_all()` will be triggered when importing locust
        from locust import main as locust_main

        print("NOTICE: gevent monkey patches have been applied !!!")
    except ImportError:
        msg = """
Locust is not installed, install first and try again.
install with pip:
$ pip install locust
"""
        print(msg)
        sys.exit(1)

import inspect
import os
from typing import List, Dict
import json

from cttest_plus.core.locustLoader import LocustLoader
from cttest_plus.utils.download import build_file, build_uuid, build_headers

""" converted pytest files from YAML/JSON testcases
"""
pytest_files: List = []

from cttest_plus.globalSetting import plus_setting, LOCUST_SETTING_FILE
from cttest_plus.utils.logger import logger

project_path = plus_setting.BASE_DIR
UUID_CONFIG = LOCUST_SETTING_FILE
locust_file = os.path.join(project_path, f'test_case/{UUID_CONFIG}_cttest_locust.json')
setting_file = os.path.join(project_path, f'test_case/{UUID_CONFIG}_projectSetting.json')
data_file = os.path.join(project_path, f'test_case/{UUID_CONFIG}_data_locust.json')
uuid_file = os.path.join(project_path, f'test_case/{UUID_CONFIG}_uuid.json')


def prepare_locust_tests() -> Dict:
    with open(locust_file, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    with open(uuid_file, 'r', encoding='utf-8') as f1:
        uuid = json.load(f1)
    locust_uuid = uuid.get('uuid', '')
    locust_tests = LocustLoader.load(raw, locust_uuid, file_uuid=UUID_CONFIG)
    return locust_tests


def prepare_locust_data() -> Dict:
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data_locust = json.load(f)
        return data_locust


def get_load_shape() -> Dict:
    with open(setting_file, 'r', encoding='utf-8') as f:
        locust_setting = json.load(f)
    return locust_setting.get("gradsLoad")


def delete_case_dir():
    """删除七天前创建的测试文件"""
    case_file_dir = project_path + '/test_case'
    if os.path.exists(case_file_dir):
        case_file_list = os.listdir(case_file_dir)
        time_now = time.time()
        for case_file in case_file_list:
            case_path = os.path.join(case_file_dir, case_file)
            create_time = os.path.getctime(case_path)
            # 计算时间差 单位：秒
            time_difference = time_now - create_time
            # 7天，秒数
            # SEVEN_DAYS = 360
            SEVEN_DAYS = 604800
            if time_difference > SEVEN_DAYS:
                # 删除文件
                print(case_path)
                if os.path.exists(case_path) and os.path.isfile(case_path):
                    logger.info(f"正在删除动态文件")
                    os.remove(case_path)


def main_locusts():
    # 删除七天前创建的文件
    delete_case_dir()

    logger.remove()
    logger.add(sys.stderr, level="WARNING")

    sys.argv[0] = "locust"
    if len(sys.argv) == 1:
        sys.argv.extend(["-h"])

    if sys.argv[1] in ["-h", "--help", "-V", "--version"]:
        locust_main.main()

    def get_arg_index(*target_args):
        for arg in target_args:
            if arg not in sys.argv:
                continue
            return sys.argv.index(arg) + 1
        return None

    # 用例文件
    url_index = get_arg_index("--url", "-u")
    url = sys.argv[url_index]
    build_file(url, f'{UUID_CONFIG}_cttest_locust.json')
    # 项目配置文件
    config_index = get_arg_index("--config", "-c")
    config = sys.argv[config_index]
    build_file(config, f'{UUID_CONFIG}_projectSetting.json')
    # uuid
    locust_uuid_index = get_arg_index("--uuid", "-u")
    locust_uuid = sys.argv[locust_uuid_index]
    build_uuid(locust_uuid, f'{UUID_CONFIG}_uuid.json')
    # 所有headers文件
    build_headers(setting_file, locust_uuid, f'{locust_uuid}_headers.json')
    # 性能测试数据文件
    data_locust_index = get_arg_index("--data_locust", "-d_l")
    if data_locust_index:
        data_locust = sys.argv[data_locust_index]
        build_file(data_locust, f'{UUID_CONFIG}_data_locust.json')
    command_index = get_arg_index("--args", "-a")
    command = sys.argv[command_index]
    command = command.replace(" ", "").split(',')
    if not config_index or not command_index:
        print("Testcase file is not specified, exit 1.")
        sys.exit(1)
    sys.argv = command
    sys.argv.extend(['-f', os.path.join(os.path.dirname(__file__), "locustfile.py")])

    locust_main.main()

