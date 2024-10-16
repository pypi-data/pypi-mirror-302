# 本模块应用于性能测试，本模块依赖driver 下HTTPDriver, KWDriver, 请确依赖驱动正常
import inspect
import uuid
from typing import List, Dict

from cttest_plus.globalSetting import plus_setting
from cttest_plus.utils.logger import logger
from cttest_plus.drivers.driverBy import DriverBy
from cttest_plus.drivers.locustDriver import HTTPDriver


class LocustDriverBy(DriverBy):
    api_request = HTTPDriver


class LocustLoader:
    task = {}

    class Task:

        def __init__(self, func, title, locust_uuid, file_uuid, **kwargs):
            self.func = func
            self.title = title
            self.kwargs = kwargs
            self.unique_uuid = locust_uuid
            self.file_uuid = file_uuid
            self.var_map = {}

        def run(self, locust_session=None, spec_data=None):

            self.func(
                **self.kwargs,
                locust_session=locust_session,
                unique_uuid=self.unique_uuid,
                file_uuid=self.file_uuid,
                var_map=self.var_map,
                spec_data=spec_data
            )

    @classmethod
    def load(cls, raw, locust_uuid, file_uuid) -> Dict:
        for spec in raw:  # 遍历测试计划列表生成可执行的测试用例
            title = spec.get("caseName")
            parametrize = spec.get("parametrize")
            weight = spec.get("weight", 1)
            # if parametrize:
            #     raise Exception(f'【格式错误】性能测试不支持TDD数据驱动，请检查用例编写格式后再继续')
            if cls.task.get(weight):
                cls.task[weight].append(cls.Task(cls.case_parse, title, locust_uuid, file_uuid, spec=spec))
            else:
                cls.task[weight] = [cls.Task(cls.case_parse, title, locust_uuid, file_uuid, spec=spec)]
        return cls.task

    @classmethod
    def case_parse(self, spec, locust_session, unique_uuid=None, file_uuid=None, var_map=None, spec_data=None):
        if not spec_data:
            spec_data = spec
        for case_node in spec_data.get("caseNodes"):
            self.node_parser(
                case_node,
                plus_setting.ANALYZE_CLASS,
                locust_session=locust_session,
                unique_uuid=unique_uuid,
                file_uuid=file_uuid,
                var_map=var_map
            )

    @classmethod
    def node_parser(cls, case_node, analyze_class, uuid=None, locust_session=None, unique_uuid=None, file_uuid=None, var_map=None):
        node_type = case_node.get("nodeType", "")
        node_body = case_node.get("nodeBody", {})

        if node_type == "BM":  # 如果节点为业务模型时 新增局部变量替换
            uuid = case_node.get("uuid")
            parent_uuid = case_node.get("parent_uuid")
            input_param = analyze_class.analyze(case_node.get("inputParam"), parent_uuid, owner_var_map=var_map)
            analyze_class.add_variable(input_param, uuid=uuid, owner_var_map=var_map)
            for step_data in node_body:
                cls.step_parse(
                    step_data,
                    analyze_class,
                    uuid=uuid,
                    var_map=var_map,
                    unique_uuid=unique_uuid,
                    file_uuid=file_uuid,
                    locust_session=locust_session
                )
            new_variable = analyze_class.analyze(case_node.get("outputParam"), owner_var_map=var_map)
            analyze_class.add_variable_from_out_param(new_variable, parent_uuid, uuid, owner_var_map=var_map)

        else:
             for step_data in node_body:
                cls.step_parse(
                    step_data,
                    analyze_class,
                    uuid=uuid,
                    locust_session=locust_session,
                    unique_uuid=unique_uuid,
                    file_uuid=file_uuid,
                    var_map=var_map
                )

    @classmethod
    def step_parse(cls, step_data, analyze_class, uuid=None, locust_session=None, unique_uuid=None, file_uuid=None, var_map=None):
        if step_data.get("nodeType"):
            cls.node_parser(
                step_data,
                analyze_class,
                uuid=uuid,
                locust_session=locust_session,
                unique_uuid=unique_uuid,
                file_uuid=file_uuid,
                var_map=var_map
            )
        else:
            kw = step_data.get('driver')
            kw_path = step_data.get("kwPath")
            data_set = step_data.get("dataSet")
            if isinstance(data_set, str): data_set = analyze_class.analyze(data_set, uuid=uuid, owner_var_map=var_map)
            host = step_data.get("host")
            model_set = step_data.get("modelSet")
            logger.info(f"kw={kw}")
            driver = getattr(LocustDriverBy, kw, None) or getattr(plus_setting.DRIVER_BY, 'user_kw')
            args = inspect.getfullargspec(driver.run).args
            l = locals()
            driver().run(**{arg: l.get(arg) for arg in args if arg not in ["cls", "self"]})
