import time
from collections import OrderedDict

import requests

from cttest_plus.drivers.basicDriver import BaseDriver
from cttest_plus.globalSetting import plus_setting
from cttest_plus.sessionManage.baseSession import BaseSession
from cttest_plus.sessionManage.requestsSession import HTTPSession
from cttest_plus.utils.compatibility import compat_request
from cttest_plus.utils.dataParser import JsonParser
from cttest_plus.utils.error import UserNotExits
from cttest_plus.utils.initTest import _Config


class HTTPDriver(BaseDriver):
    header = plus_setting.HTTP_REQUEST_HEADER
    session_class = HTTPSession

    @classmethod
    def run(cls, data_set, model_set, uuid=None, host='', locust_session=None):
        host = host or _Config.environment.get("default")
        if data_set.get("version") == 2:
            pass
        else:  #  此处做新的版本兼容
            data_set = compat_request(data_set)
        user = data_set.get("session")
        http_session = cls.session_class.get_session(user, locust_session=locust_session)
        req_query = cls.analyze(data_set.get("req_query") or {}, uuid)  or {}# 参数化求数据
        req_body = cls.analyze(data_set.get("req_body") or {}, uuid) or {}
        headers = cls.analyze(data_set.get("headers") or {}, uuid) or {}
        sleep = data_set.get('sleep')
        if sleep: time.sleep(sleep)
        method = model_set.get("method")
        path = model_set.get("path")
        req_body_type = model_set.get("req_body_type") or model_set.get("dataType")
        if data_set.get("key_path"):
            path = path.format(**data_set.pop("key_path"))
        http_session.headers.update(headers)
        response = cls.session_class.send( # 发送session会话请求
            http_session,
            method=method,
            url=cls.analyze(host+path, uuid),
            params = req_query,
            **cls.request_param_type_match(req_body, req_body_type)
        )
        try:
            cls.check(data_set.get("assert", {}), response, uuid=uuid)  # 执行数据断言操作
            extract_content = data_set.get("extract") or {}
            cls.extract(response, extract_content, uuid) or {}  # 执行保存变量操作
        except Exception as e:
            raise e

    @classmethod
    def request_param_type_match(cls, request_data, req_body_type):
        if req_body_type == "form":
            data = {"data": request_data}
            return data
        elif req_body_type in ["raw", "json"]:
            data = {"json": request_data}
            return data
        elif req_body_type == "file":
            data = {"files": request_data}
            return data
        return {}



class LocustSession(BaseSession):

    session_list = OrderedDict()
    session_type = "httpUser"
    http_user_code = {}

    @classmethod
    def new_session(cls, session_name, locust_session=None):
        """
        新建会话
        :param session_name: 会话名称/用户名称
        :param build_content: "httpUser"用户登录配置
        :return: None
        """
        if not cls.session_list:
            cls.http_session_config = cls.session_config.get(cls.session_type)
            cls.build_type = cls.http_session_config.get("build_type", "yaml")
        if cls.build_type == "yaml":
            build_content = cls.http_session_config.get("yaml_user").get(session_name)
            cls.build_session_by_step(session_name, build_content, locust_session=locust_session)
        elif cls.build_type == "code":
            cls.build_session_by_code(session_name, locust_session=locust_session)
        else:
            raise NotImplemented(f"【登录方式】登录类型错误暂时不支持该类型登录")

    @classmethod
    def build_session_by_code(cls, session_name, locust_session=None):
        if cls.http_user_code:
            pass
        else:
            code_string = cls.session_config.get("codeString")
            exec(code_string, cls.http_user_code)
        if "HttpUser" in cls.http_user_code and hasattr(cls.http_user_code["HttpUser"], session_name):
            cls.session_list[session_name] = getattr(cls.http_user_code["HttpUser"], session_name)()
        else:
            raise UserNotExits(f"【用户错误】用户名：{session_name} 不存在，请检查项目登录配置是否添加该用户")

    @classmethod
    def build_session_by_step(cls, session_name, step_data, locust_session=None):

        if isinstance(step_data, str) and step_data.startswith('$'):
            session = JsonParser.analyze(step_data)
            if locust_session:
                locust_session.headers = session.headers
                session = locust_session
        else:
            session = locust_session or requests.session()
            for login_step in step_data:
                login_step = JsonParser.analyze(login_step)
                method = login_step.get('method')
                session.headers.update(login_step.get('header'))
                url = login_step.get('url')
                body_type = login_step.get("bodyType", '')
                data = login_step.get("data", {})
                extract = login_step.get("extract")
                if method.lower() == "get":
                    response = session.request(url=url, method='get', params=data)
                elif body_type in ['raw', "json"]:
                    response = session.request(url=url, method=method, json=data)
                else:
                    response = session.request(url=url, method=method, files=data)
                JsonParser.extract(extract, response)
        cls.session_list[session_name] = session

    @classmethod
    def send(cls, session, **kwargs):
        response = session.request(**kwargs)
        return response
