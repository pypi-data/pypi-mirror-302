import inspect
import time
from typing import Dict

from cttest_plus.assert_.web import WEBAssert
from cttest_plus.drivers.basicDriver import BaseDriver
from cttest_plus.sessionManage.appSession.appiumSession import APPSession
from cttest_plus.utils.dataParser import patch_expr


class APPDriver(BaseDriver):
    session_class = APPSession
    assert_class = WEBAssert

    @classmethod
    def run(cls, data_set, uuid, host, **kwargs):
        """
        Webdriver驱动执行浏览器元素定位与元素动作操作
        :param data_set: 测试用例节点信息
            {
            "path": "/login",
            "user": "user1",
            "version": 2,
            "request": [
                {"eventName": "元素点击", "event": "click", "locations": ["css selector", "#kw"], "input": "输入内容"},
                {"eventName": "元素名称", "event": "click", "locations": ["xpath", "#btn"], "input": "输入内容"},
                {"eventName": "元素名称", "event": "click", "locations": [], "input": "输入内容"},
                {"eventName": "键盘输入", "event": "key_event", "input": "回车/其他" },
                {"eventName": "元素移动", "event": "move_to_element", "location": ["id", "kw"], "target": ["id", "kw"]},
                {"eventName": "元素移动", "event": "move_to_point", "location": ["id", "kw"], "target": [1, 2]},
                {"eventName": "鼠标移动", "event": "mouse_hover", "target": ["id", "kw"]},
                {"eventName": "鼠标移动", "event": "mouse_move", "target": [1, 2]},
                {"eventName": "标签属性保存", "event": "get_tag_attr", "location": [["id", "kw", []]], "attr": ["name", "alias_name"]},
                {"eventName": "标签属性变更", "event": "set_tag_attr", "location": [["id", "kw", []]], "attr": ["name", "value"]}
            ],
            "assert": {"ele_exits":["css", "#id"], "title_exits": "title", 'eq': ["@{alias_name}", "expect_value"],...}
            }
        :param uuid: 模型的uuid
        :return:
        """
        request = data_set.get("request")
        user = data_set.get("user")
        sleep = data_set.get('sleep', 0)
        if user:
            username = cls.analyze(user, uuid)
            driver = cls.analyze_class.get_user(username)

        else:
            user = data_set.get("session")
            driver = cls.session_class.get_session(user)

        for step in request:  # 执行web UI操作
            driver = cls.session_class.send(step, driver, cls.analyze_class, uuid=uuid)

        assert_ = data_set.get("assert", [])
        # 转义断言表达式，提取需要断言的内容
        cls.translate_assert(assert_, driver)
        # 执行用例断言
        cls.check(assert_, driver)
        time.sleep(sleep)

    @classmethod
    def translate_assert(cls, assert_content: Dict, response, **kwargs):
        """断言表达式文本提取"""
        assert_content = cls.analyze(assert_content, kwargs.get("uuid"))
        for assert_line in assert_content:
            for comparator, value in assert_line.items():
                if comparator in ['ele_exits', 'title_exits', 'url_exits']:
                    cls.assert_class().validate(comparator, response, value)
                else:
                    translate_content = patch_expr(response, value[0])
                    result = translate_content[0] if translate_content else "不存在的内容"
                    cls.assert_class().validate(comparator, result, value[1])
