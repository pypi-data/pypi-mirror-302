import importlib
import json
import types
from typing import Dict, AnyStr
import threading
import pluggy

import requests
from moviepy.editor import *

from cttest_plus.globalSetting import plus_setting, DYNAMIC_VERIFY_FIlE
from cttest_plus.utils.logger import logger
from cttest_plus.utils.dataParser import GlobalVariableMap
from . import hookspec

class _Config:
    session_config: Dict = {}
    platform_host: AnyStr = ""
    environment: Dict = {}
    headers: Dict = {}
    version: int = 1
    code_string: str = ""
    first_tier: str = ""
    verify_content = {}
    case_source = 0
    traceback = ""

    @classmethod
    def add_hookimpl(cls):
        pm = pluggy.PluginManager('cttest')
        pm.add_hookspecs(hookspec)
        cls.module = importlib.import_module('hookimpl')
        pm.register(cls.module)

    @classmethod
    def set_config(cls, raw):
        cls.add_hookimpl()
        cls.session_config = raw.get("loginSetting")
        cls.environment = raw.get("environment")
        cls.headers = raw.get("header")
        cls.platform_host = raw.get('platformHost', "127.0.0.1")
        cls.code_string = raw.get("codeString", "pass")
        cls.first_tier = raw.get("firstTier", True)
        GlobalVariableMap.var_map['_run_env_'] = raw.get('runEnv')
        cls.verify_content = cls.read_verify()

    @classmethod
    def load_func(cls):
        LoadFunction.load_builtin_func()  # 加载CTtest plus的内置函数
        LoadFunction.load_project_func()
    
    @staticmethod
    def read_verify():
        try:
            with open(plus_setting.BASE_DIR + "/test_case/" + DYNAMIC_VERIFY_FIlE, 'r', encoding='utf8') as f:
                verify_content = json.loads(f.read(), encoding='utf8')
            return verify_content
        except Exception as e:
            logger.warning(f"【无法加载契约文件】: {e}")
            return {}


class LoadFunction:
    @classmethod
    def load_module_functions(cls, module):
        for name, item in vars(module).items():
            if isinstance(item, types.FunctionType):
                GlobalVariableMap.func_map[name] = item
            elif name == "CLASS_MAP":
                GlobalVariableMap.class_map.extend(item)

    @classmethod
    def load_builtin_func(cls, module='cttest_plus._miracle'):
        """
        获取指定文件的函数视图
        :param module:
        :return:
        """
        imported_module = importlib.import_module(module)
        imported_module = importlib.reload(imported_module)
        return cls.load_module_functions(imported_module)

    @classmethod
    def load_project_func(cls):
        try:
            logger.info(f'【加载miracle】:正在加载，miracle.py文件函数')
            imported_module = importlib.import_module('miracle')
            imported_module = importlib.reload(imported_module)
            cls.load_module_functions(imported_module)
        except ModuleNotFoundError:
            logger.warning(f'【加载miracle】:项目文件未添加miracle.py文件')

    @classmethod
    def load_func_from_code_string(cls, code_string):
        """
        通过加载远程平台字符串代码来加载函数
        :param code_string: eg.
            def func_name(*args, **kwargs):
                # make your own magic func here
                return "your expect value"
        :return: None
        """

        exec(code_string+"\npass")
        for name, item in locals().items():
            if isinstance(item, types.FunctionType):
                GlobalVariableMap.func_map[name] = item
            elif name == "CLASS_MAP":
                GlobalVariableMap.class_map.extend(item)


class RunningSummery:
    # run_record = {"case_name": {"user1": [2, 10]}, "case": {"user1": [10, 20]}}
    # start_time = {"user1": 1.1}
    # video_info = {"user1": {"host": "10.118.71.154", "video_name": 'chrome_88.0_48e3d752015111ec87ae286ed48a3c66.mp4'}}
    build_info = {}
    run_record = {}
    start_time = {}
    video_info = {}

    def __init__(self, video_path):
        self.video_path = video_path
        self.video_list = []
        for user, video_detail in self.video_info.items():
            video_url = video_detail.get('host')+':4444/video/'+video_detail.get("video_name")
            new_video_name = video_path + '/' + str(int(self.start_time.get(user)))+'.mp4'
            self.build_info[user] = new_video_name
            if not os.path.exists(video_path):
                os.mkdir(video_path)
            self.video_list.append(new_video_name)
            self._do_load_media(video_url, new_video_name)

    def clip_video(self):
        if plus_setting.NEED_VIDEO:
            t_list = []
            for case_name, user_item in self.run_record.items():
                for user_name, timestamp in user_item.items():
                    if user_name.startswith('global:') or user_name.startswith('g:'):
                        user_name = user_name.split(':')[1]
                        start = timestamp[0] - self.start_time.get(user_name)
                        end = timestamp[1] - self.start_time.get(user_name)
                        t = threading.Thread(
                            target=self._write_video,
                            args=(user_name, start if start > 0 else 0, end, str(timestamp[0]).replace('.', '') + '.mp4')
                        )
                        t_list.append(t)
            for t in t_list:
                t.start()
            for t in t_list:
                t.join()

    def _write_video(self, user, start, end, video_name):
        video_clip = VideoFileClip(self.build_info[user]).subclip(int(start), int(end))
        video_content = CompositeVideoClip([video_clip])
        video_content.write_videofile(self.video_path + '/' + video_name)

    @staticmethod
    def _do_load_media(url, path):
        try:
            pre_content_length = 0
            while True:
                res = requests.get(url, stream=True)
                headers = {}
                if os.path.exists(path):
                    headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
                content_length = int(res.headers['content-length'])
                if content_length < pre_content_length or (
                        os.path.exists(path) and os.path.getsize(path) == content_length) or content_length == 0:
                    break
                pre_content_length = content_length
                with open(path, 'ab') as file:
                    file.write(res.content)
                    file.flush()
                    print('下载成功,file size : %d   total size:%d' % (os.path.getsize(path), content_length))
        except Exception as e:
            print(e)
        
    

# RunningSummery().clip_video()

