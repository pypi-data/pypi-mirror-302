"""
This module handles compatibility issues between testcase format v1 and v2.
"""
from cttest_plus.utils.error import CompatError
from cttest_plus.utils.logger import logger
"""
断言版本兼容
"""


def compat_assert(assert_content):
    """
    version 1 >>> version 2
    version1:
        [
            {"assert_name": "status_code", "assert_mode": "eq", "assert_value": 201}
        ]
    version2:
        [
            {"eq": ["status_code", 201]}
        ]
    :param assert_content:
    :return: 版本2的断言列表
    """
    return [{
        item["assert_mode"]: [item["assert_name"], item["assert_value"]]}
        for item in assert_content if item.get("assert_mode")
    ]


"""
保存变量版本兼容
"""

def compat_extract(extract):
    """
    version 1 >>> version 2
    version1:
        [
            {"variable_name": "", "variable_expression": "", "variable_type": "", "default": ""}
        ]
    version2:
        [
            ["patch_type:expresion", "alias", "default"],
            'key/expression'
        ]
    :param extract: 保存内容
    :return:
    """
    new_extract = []
    for item in extract:
        variable_type = item.get("variable_type")
        variable_expression = item.get("variable_expression")  # type: str
        variable_name = item.get("variable_name")
        default = item.get("default")

        if not variable_expression:
            continue
        elif not variable_type:
            item_extract = [variable_expression, variable_name]
        elif variable_type == "class":
            item_extract = ["$", variable_name]
        elif variable_type == "reg":
            item_extract = ["reg:" + variable_expression, variable_name]
        elif variable_type == "json":
            item_extract = [variable_expression, variable_name]
        elif variable_type == "xpath":
            item_extract = ["xpath:" + variable_expression, variable_name]
        else:
            raise CompatError(
                f"【版本兼容】提取对象返回值时版本兼容出错，获得了一个extract={variable_type}。期望获取的extract in "
                f"[class reg json xpath $]"
            )
        if default != None:
            item_extract.append(default)
        new_extract.append(item_extract)
    return new_extract


"""
请求数据版本兼容
"""

def compat_request(data_set):
    """
    请求数据版本兼容
    version1 >>> version2
    version1:
        {
            "request": {
                "user": "user1",
                "test_data": {
                    "req_headers": "",
                    "req_query": "",
                    "req_params": "",
                    "req_body": "",
                    "sleep": 5,
                    }
                }
            "response": {
                "variable": [],
                "assert": []
            }
        }
    version2:
        {
            "version": 2,
            "user": "user1",
            "session": "user1",
            "headers": {}
            "request": {"key_path": {"id": 1}, "kwy": "value"},
            "sleep": 5
            "extract": [],
            "assert": [],
        }
    :param data_set: 测试用例json数据
    :return: version2版本请求数据结构
    """
    new_body = {"request":{}}
    new_body["version"] = 2
    request = data_set.get("request")
    new_body["user"] = request.get("user")
    new_body["session"] = request.get("session")
    test_data = request.get("test_data")
    if test_data:
        new_body["req_query"] = test_data.get("req_query", {})
        new_body["req_body"] = test_data.get("req_body", {})
        new_body["headers"] = test_data.get("req_headers", {})
        new_body["sleep"] = test_data.get("sleep") or request.get("sleep")
        new_body["retry"] = request.get("retry_num")
        new_body["delay"] = request.get("retry_delay")
        if test_data.get("req_params"):
            new_body["key_path"] = test_data.get("req_params")
        if test_data.get("sleep"):
            new_body["sleep"] = test_data.get("sleep")
    response = data_set.get("response", {})
    if response.get("variable"):
        new_body["extract"] = compat_extract(response.get("variable"))
    if response.get("assert"):
        new_body["assert"] = compat_assert(response.get("assert"))
    return new_body


"""
关键字请求数据兼容
"""


def compat_kw_request(data_set, kw):
    """
    关键字数据兼容
    version1 >>> version2
    version1:
        {
            "request": {
                "user": "user1",
                "test_data": {
                  "username": "mandy",
                  "password": "Init@1125!@#$"
                }
            },
            "response": {
                "assert": [],
                "variable": [
                    {
                        "variable_type": "",
                        "variable_expression": "",
                        "variable_name": ""
                    }
                ]
            }
        }
    version2:
        {
            "user": "",
            "request": {},
            "extract": []
        }
    """
    new_body = {}
    # kw = kw.replace("keywords", "kword") if kw else "kword"
    new_body["user"] = data_set.get("request").get("user")
    new_body["request"] = data_set.get("request").get("test_data")
    new_body["extract"] = compat_extract(data_set.get("response").get("variable"))
    new_body["assert"] = compat_assert(data_set.get("response").get("assert") or [])
    return new_body, kw


def compat_ui_request(data_set):
    """
    # UI请求数据兼容
    # version1 >> > version2
    version1:
        {
            "path": "/login",
            "user": "user1",
            "version": "",
            "request": [
                {
                    "action": "send_keys",
                    "eleName": "账号输入框",
                    "location": [["ID", "username", [None, None]]],
                    "input": ["A02441"]
                },
                {
                    "action": "move_ele",
                    "eleName": "密码输入框",
                    "location": [["ID", "password", [None, None]]],
                    "input": ["Xu173798"]
                },
                {
                    "action": "click",
                    "eleName": "登录按钮",
                    "location": [["OCR", "登录",[None,None]]],
                    "input": []
                }
            ]
        }
    version2:
        {
            "path": "/login",
            "user": "user1",
            "version": 2,
            "request": [
                {"event": ""},
                {},
                {}
            ]
        }
    """
    data_set["version"] = 2
    request = data_set.get("request")

    for step in request:
        event = step.get("action")
        if hasattr(EventCompat, event):
            event, rename, index = getattr(EventCompat, event)
            step["event"] = event
            if rename:
                logger.info(f"event={event}, rename={rename}, index={index}, step={step}")
                if index == 'all':
                    step[rename] = step["input"]
                else:
                    step[rename] = step["input"][index]


class EventCompat:
    click = ("click", "", "")
    send_keys = ("input", "input", 0)
    select_by_value = ("select_by_value", "input", 0)
    select_by_index = ("select_by_index", "input", 0)
    switch_to_tab = ("switch_to_new_window", "", '')
    clear = ("clear", "", "")
    move_to_element = ("move_to_element", "", "")
    tap_screen = ("useless", "", "")
    assert_elm_displayed = ("ele_exits", "", "")
    assert_elm_text = ("text_exits", "attr", 0)
    switch_to_default_tab = ("switch_to_default_tab", "", "")
    swipe_screen = ("swipe_screen", "input", "all")
    swipe_screen_to_elm_visable = ("scroll_into_view", "", "")  # 滑动屏幕至元素可见(app专用)
    get_elm_text = ("get_elm_text", "attr", 0)
    right_click = ("right_click", "", "")
    click_if_exists = ("click_if_exits", "", "")
    scroll_screen = ("swipe_screen", "", "")
    assert_elm_not_displayed = ("not_displayed", "", "")
