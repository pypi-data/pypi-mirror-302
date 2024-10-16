import time
from typing import Dict

from appium.webdriver.webdriver import WebDriver as AppDriver

from cttest_plus.utils.logger import logger
from cttest_plus.assert_.web import WEBAssert
from cttest_plus.drivers.basicDriver import BaseDriver
from cttest_plus.globalSetting import plus_setting
from cttest_plus.sessionManage.webSession.seleniumSession import WEBSession
from cttest_plus.utils.compatibility import compat_ui_request
from cttest_plus.utils.dataParser import patch_expr
from cttest_plus.drivers.compatorDriver import CompatWEBDriver
from cttest_plus.drivers.appDriver import APPDriver
from cttest_plus.utils.initTest import RunningSummery
from cttest_plus.utils.initTest import _Config


def run_time(func):
    """
    记录每条UI用例执行时间
    :param func:
    :return:
    """
    def inner(cls, data_set, uuid, host, case_name, **kwargs):
        # 用于记录用例运行时间
        user = data_set.get("user")
        if not user.startswith('g:') and not user.startswith('global:'):
            return func(cls, data_set, uuid, host, case_name, **kwargs)

        if not RunningSummery.run_record.get(case_name):
            RunningSummery.run_record[case_name] = {}
        case_record = RunningSummery.run_record[case_name].get(user)
        if not case_record:
            RunningSummery.run_record[case_name][user] = [time.time()]
        try:
            return func(cls, data_set, uuid, host, case_name, **kwargs)
        finally:
            if len(RunningSummery.run_record[case_name][user]) < 2:
                RunningSummery.run_record[case_name][user].append(time.time())
            else:
                RunningSummery.run_record[case_name][user][1] = time.time()
    return inner


class WEBDriver(BaseDriver):
    session_class = WEBSession
    assert_class = WEBAssert

    @classmethod
    @run_time
    def run(cls, data_set, uuid, host, case_name, **kwargs):
        """
        Webdriver驱动执行浏览器元素定位与元素动作操作
        :param host:
        :param case_name:
        :param kwargs:
        :param data_set: 测试用例节点信息
            {
                "path": "/login",
                "user": "user1",
                "version": 2,
                "request": [
                    {"eventName": "元素点击", "event": "click", "locations": ["css selector", "#kw"]},
                    {"eventName": "输入内容", "event": "input", "locations": [["xpath", "#btn", []]], "input": "输入内容"},
                    {"eventName": "打开网页", "event": "open", "url": "输入内容"},
                    {"eventName": "键盘输入", "event": "key_event", "input": "回车/其他" },
                    {"eventName": "元素移动", "event": "move_to_element", "location": ["id", "kw"], "target": ["id", "kw"]},
                    {"eventName": "元素移动", "event": "move_to_point", "location": ["id", "kw"], "target": [1, 2]},
                    {"eventName": "鼠标移动", "event": "mouse_hover", "target": ["id", "kw"]},
                    {"eventName": "标签属性保存", "event": "get_tag_attr", "location": ["id", "kw"], "attr": ["expr", "alias_name"]},
                    {"eventName": "标签属性变更", "event": "set_tag_attr", "location": ["id", "kw"], "attr": ["name", "value"]},
                ],
                "assert": [
                    {"ele_exits":["css", "#id"]},
                    {"title_exits": "title"},
                    {'eq': ["xpath://*[@name='小明']::value", "expect_value"]},...
                ]
            }
        :param uuid: 模型的uuid
        :return:
        """
        host = host or _Config.environment.get("default")
        if data_set.get('version') != 2:
            compat_ui_request(data_set)
        request = data_set.get("request")
        user = data_set.get("user")  # type: str

        if user.startswith('global:') or user.startswith('g:'):
            browser = cls.session_class.get_session(user.split(':')[1])
        else:
            username = cls.analyze(user, uuid)
            browser = cls.analyze_class.get_user(username)

        if isinstance(browser, AppDriver):
            APPDriver.run(data_set, uuid, host, **kwargs)
        else:
            path = data_set.get('path').replace(' ', '')
            sleep = data_set.get('sleep', 0)
            if path:
                time.sleep(2)
                url = cls.analyze(host+path, uuid=uuid)
                logger.info(f"【打开网址】正在打开网址：{url}")
                browser.get(url)

            for step in request:  # 执行web UI操作
                cls.session_class.send(step, browser, cls.analyze_class, uuid)
            assert_ = data_set.get("assert", [])
            cls.check(assert_, browser, uuid=uuid)
            time.sleep(sleep)

    @classmethod
    def check(cls, assert_content: Dict, response, **kwargs):
        assert_content = cls.analyze(assert_content, kwargs.get("uuid"))
        for assert_line in assert_content:
            for comparator, value in assert_line.items():
                if comparator in ['ele_exits', 'title_exits', 'url_exits']:
                    cls.assert_class().validate(comparator, response, value)
                else:
                    translate_content = patch_expr(response, value[0])
                    result = translate_content[0] if translate_content else "不存在的内容"
                    cls.assert_class().validate(comparator, result, value[1])
