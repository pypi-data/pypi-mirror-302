import inspect

import allure

from cttest_plus.globalSetting import plus_setting
from cttest_plus.utils.logger import logger
from cttest_plus.utils.compatibility import compat_assert
from cttest_plus.drivers.basicDriver import BaseDriver

class NodeParser:
    node_info = {}
    node_data = []
    case_name = ""
    @classmethod
    def node_parser(cls, case_node, analyze_class, uuid=None):
        if not case_node:
            return
        node_type = case_node.get("nodeType", "")
        node_name = case_node.get("nodeName", "")
        node_body = case_node.get("nodeBody", {})
        check_content = compat_assert(case_node.get("check", {}))
        check_result = True
        try:
            BaseDriver.check(check_content, response={})
        except AssertionError:
            check_result = False
        node_doc = f"【{node_type}】√ {node_name}" if check_result else f"【{node_type}】X {node_name}"
        if node_type == "BM":  # 如果节点为业务模型时 新增局部变量替换
            logger.info(f"【业务模型】业务执行， 模型名称BM={node_name}")
            uuid = case_node.get("uuid")
            parent_uuid = case_node.get("parent_uuid")
            logger.info(f"【业务模型】业务执行， 业务模型入参参数化，inputParam={case_node.get('inputParam')}")
            input_param = analyze_class.analyze(case_node.get("inputParam"), parent_uuid)
            analyze_class.add_variable(input_param, uuid=uuid)

            with allure.step(node_doc):
                for step_data in node_body:
                    cls.step_parse(step_data, analyze_class, uuid)
            new_variable = analyze_class.analyze(case_node.get("outputParam"))
            analyze_class.add_variable_from_out_param(new_variable, parent_uuid, uuid)
            analyze_class.remove_local_variable(uuid) # 清除局部变量
        else:
            with allure.step(node_doc):
                if check_result:
                    for step_data in node_body:
                        cls.step_parse(step_data, analyze_class, uuid)

    @classmethod
    def step_parse(cls, step_data, analyze_class, uuid=None):
        """
        执行节点下每个步骤测试数据
        :param step_data: 节点下测试步骤数据
            Example:
                {
                    "stepName": "测试步骤名称",
                    "driver": "测试步骤关键字",
                    "modelSet":{},
                    "dataId": 1,
                    "host": "https://saasdemo.s2.ewewo.com/Center2Service",
                    "dataSet": {}
                }
            dataSet节点测试数据集
        :return: None
        """
        if step_data.get("nodeType"):
            cls.node_parser(step_data, analyze_class, uuid)
        else:
            with allure.step(f"{step_data.get('stepName', 'unnamed')}"):
                logger.info(f"{'='*10}{step_data.get('stepName', 'unnamed')}{'='*10}")
                kw = step_data.get('driver')
                kw_path = step_data.get("kwPath")
                data_set = step_data.get("dataSet")
                case_name = cls.case_name
                if isinstance(data_set, str): data_set = analyze_class.analyze(data_set)
                host = step_data.get("host")
                process_id = step_data.get("processId")
                model_set = step_data.get("modelSet")
                driver = getattr(plus_setting.DRIVER_BY, kw, None) or getattr(plus_setting.DRIVER_BY, 'user_kw')
                args = inspect.getfullargspec(driver.run).args
                l = locals()
                driver().run(**{arg: l.get(arg) for arg in args if arg not in ["cls", "self"]})
