# _*_encoding=utf8_*_
# @Time : 2021/6/1 11:30 

# @Author : xuyong

# @Email: yong1.xu@casstime.com
import requests

from cttest_plus.sessionManage.baseSession import BaseSession
from cttest_plus.utils.error import UserNotExits
from cttest_plus.utils.dataParser import JsonParser

class HTTPSession(BaseSession):
    """
    一个用于管理Http会话的类
    """
    session_list = []
    session_type = "httpUser"
    http_user_code = {}

    @classmethod
    def new_session(cls, session_name, on_session=None):
        if not cls.session_list:
            cls.http_session_config = cls.session_config.get(cls.session_type)
            cls.build_type = cls.http_session_config.get("build_type", "yaml")

        if cls.build_type == "yaml":
            build_content = cls.http_session_config.get(session_name)
            cls.build_session_by_step(session_name, build_content, session=on_session)
        elif cls.build_type == "code":
            cls.build_session_by_code(session_name, session=on_session)
        else:
            raise NotImplemented(f"【登录方式】登录类型错误暂时不支持该类型登录")

    @classmethod
    def get_session(cls, session_name, on_session=None):
        session = cls.session_list.get(session_name)

        if session:
            return session
        else:
            cls.new_session(session_name, on_session=on_session)
            return cls.session_list.get(session_name)

    @classmethod
    def build_session_by_code(cls, session_name, session=None):
        if cls.http_user_code:  # 判断是否执行过code_string
            pass
        else:
            code_string = cls.session_config.get("codeString")
            exec(code_string, cls.http_user_code)
        if "HttpUser" in cls.http_user_code and hasattr(cls.http_user_code["HttpUser"], session_name):
            cls.session_list[session_name] = getattr(cls.http_user_code["HttpUser"], session_name)()
        else:
            raise UserNotExits(f"【用户错误】用户名：{session_name} 不存在，请检查项目登录配置是否添加该用户")

    @classmethod
    def build_session_by_step(cls, session_name, step_data, session=None):
        session = session or requests.session()
        for login_step in step_data:
            login_step = JsonParser.analyze(login_step)
            method = login_step.get('method')
            header = session.headers.update(login_step.get('header'))
            url = login_step.get('url')
            body_type = login_step.get("bodyType")
            data = login_step.get("data")
            extract = login_step.get("extract")
            if body_type in ['raw', "json"]:
                response = session.request(url=url, method=method, headers=header, json=data)
            else:
                response = session.request(url=url, method=method, headers=header, files=data)
            JsonParser.extract(extract, response)
        cls.session_list[session_name] = session

    @classmethod
    def close_session(self):
        """ http 会话不需要断开连接 """
        pass