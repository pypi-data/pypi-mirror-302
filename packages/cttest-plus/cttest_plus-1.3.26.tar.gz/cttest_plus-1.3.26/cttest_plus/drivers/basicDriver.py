import re
import json
from abc import ABCMeta, abstractmethod
from json import JSONDecodeError
from typing import Dict

from cttest_plus.assert_.publicAssert import AssertFactory
from cttest_plus.sessionManage.baseSession import BaseSession
from cttest_plus.utils.dataParser import patch_expr, JsonParser
from cttest_plus.utils.logger import logger
from cttest_plus.globalSetting import plus_setting

body_compile = re.compile('^body\.')


class BaseDriver(metaclass=ABCMeta):
    analyze_class = JsonParser
    assert_class = AssertFactory
    session_class = BaseSession

    @classmethod
    @abstractmethod
    def run(cls, *args, **kwargs):
        pass
    
    @classmethod
    def analyze(cls, raw_data, uuid=None, var_map=None):
        raw_data = cls.analyze_class.analyze(raw_data, uuid, owner_var_map=var_map)
        return raw_data

    @classmethod
    def extract(cls, response, extract_list, uuid=None, var_map=None):
        try:
            return cls.analyze_class.extract(extract_list, response, uuid, owner_var_map=var_map)
        except JSONDecodeError as e:
            logger.error(f"【变量提取错误】接口返回结果为非json结构，无法保存表达式结果")
            raise e

    @classmethod
    def check(cls, assert_content: Dict, response, **kwargs):
        """
        将表达式
        :param assert_content:
            Example:
                [
                    {"eq": ["返回结果提取表达式", "期望返回结果", "错误消息提示"]},
                    {"eq": ["实际返回结果", "期望返回结果", "断言错误时返回消息提示"]},
                    {"eq": ["status_code", "200", "接口返回状态码不等于200"]},
                    {"lt": ["id", "123", "接口返回状态码不等于200"]},
                ]
            官方文档： 飞熊社区XXX
        :param response:
            接口返回的response对象
        :return: dict 经过解析后的断言文本内容
        """
        assert_content = cls.analyze(assert_content, kwargs.get("uuid"), kwargs.get("var_map"))
        for assert_line in assert_content:
            for comparator, value in assert_line.items():
                # 兼容代码
                extract_value = cls.analyze_class.get_variable(var_name=value[0], uuid=kwargs.get("uuid"), owner_var_map=kwargs.get("owner_var_map"))
                if type(value[0]) == str:
                    value[0] = body_compile.sub('', value[0]) # 去掉匹配中的body. 兼容cttest1版本
                try :
                    translate_content = patch_expr(response, value[0]) or extract_value
                    result = translate_content[0] if isinstance(translate_content, list) and translate_content else translate_content
                except Exception as e:
                    logger.error(f'【断言表达式】表达式格式错误，请检查表达式语法是否符合规范')
                    if plus_setting.PRINT_RESPONCE:
                        logger.info(f"【返回数据】: response={response}")
                    raise e
                logger.info(f"【结果断言】constant={translate_content} {type(result)}{result} {comparator}  {value[1]}{type(value[1])}")
                cls.assert_class().validate(comparator, result, value[1])

        return assert_content

    @classmethod
    def close(cls):
        pass
