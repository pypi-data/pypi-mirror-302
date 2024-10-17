import json
import requests

from cttest_plus.core.nodeParser import NodeParser
from cttest_plus.utils.logger import logger
from cttest_plus.globalSetting import plus_setting
from cttest_plus.utils.initTest import _Config
from ..tool.step import Step
from ..miracle import get_model, get_data


class TestCase(Step):

    def test_01(self):
        logger.info(f"本地测试用例1：访问百度")
        res = requests.get(url='http://www.baidu.com')
        logger.info(res)

    def test_02(self):
        logger.info(f"本地测试用例2：api用例")
        # 读配置文件
        with open(plus_setting.BASE_DIR + f'/test_case/projectSetting.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        _Config.set_config(config)
        # 读用例文件
        with open(plus_setting.BASE_DIR + f'/test_case/cttest_api.json', 'r', encoding='utf-8') as f:
            case_list = json.load(f)
        # 跑用例
        for spec in case_list:
            parametrize = spec.get("parametrize")
            if parametrize:
                for param in parametrize:
                    plus_setting.ANALYZE_CLASS.add_variable(param)
                    case_nodes = spec.get("caseNodes")
                    NodeParser.case_name = spec.get('caseName') + str(spec.get('caseId'))
                    for case_node in case_nodes:
                        NodeParser.node_parser(case_node, plus_setting.ANALYZE_CLASS)
            else:
                case_nodes = spec.get("caseNodes")
                NodeParser.case_name = spec.get('caseName') + str(spec.get('caseId'))
                for case_node in case_nodes:
                    NodeParser.node_parser(case_node, plus_setting.ANALYZE_CLASS)


    def test_03(self):
        logger.info(f"本地测试用例3：ui用例")
        # 读配置文件
        with open(plus_setting.BASE_DIR + f'/test_case/projectSetting.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        _Config.set_config(config)
        # 读用例文件
        with open(plus_setting.BASE_DIR + f'/test_case/cttest_web.json', 'r', encoding='utf-8') as f:
            case_list = json.load(f)
        # 跑用例
        for spec in case_list:
            parametrize = spec.get("parametrize")
            if parametrize:
                for param in parametrize:
                    plus_setting.ANALYZE_CLASS.add_variable(param)
                    case_nodes = spec.get("caseNodes")
                    NodeParser.case_name = spec.get('caseName') + str(spec.get('caseId'))
                    for case_node in case_nodes:
                        NodeParser.node_parser(case_node, plus_setting.ANALYZE_CLASS)
            else:
                case_nodes = spec.get("caseNodes")
                NodeParser.case_name = spec.get('caseName') + str(spec.get('caseId'))
                for case_node in case_nodes:
                    NodeParser.node_parser(case_node, plus_setting.ANALYZE_CLASS)

    # def test_04(self):
    #     self.step(
    #         'api',
    #         data_set=get_data('Sheet1.a1', source='excel'),
    #         model_set={'method': "get", "path": "/api", "req_body_type": "json"}
    #     )
    #     self.step('api', data_set=get_data('Sheet1.a2', source='excel'), model_set=get_model(123))
    #     self.step('web', data_set={})
    #     self.step('app', data_set={})

