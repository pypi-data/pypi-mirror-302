import os
import traceback

import allure
import pytest
import yaml
import json

from cttest_plus.core.nodeParser import NodeParser
from cttest_plus.globalSetting import plus_setting, DYNAMIC_FILE, DYNAMIC_SETTING_FILE
from cttest_plus.utils.logger import logger
from cttest_plus.utils.initTest import _Config, RunningSummery
from cttest_plus.utils.grammarCheck import CheckResult


plus_setting.TEST_FILES.append(DYNAMIC_FILE)


def pytest_collect_file(parent, path):
    if path.ext == ".json" and path.basename in plus_setting.TEST_FILES:
        return TestFile.from_parent(parent, fspath=path)
    elif path.ext == '.json' and path.basename == DYNAMIC_SETTING_FILE:
        with open(plus_setting.BASE_DIR + f'/test_case/{DYNAMIC_SETTING_FILE}', 'r', encoding='utf-8') as f:
            config = json.load(f)
        _Config.set_config(config)


class Level:
    P0 = "blocker"
    P1 = "critical"
    P2 = "normal"
    P3 = "minor"
    P4 = "trivial"


class TestFile(pytest.File):
    def collect(self):
        first_tier = _Config.first_tier
        case_list = json.load(self.fspath.open(mode="r", encoding="utf-8"))
        # 初始化项目信息
        case_source = 0 if len(case_list) > 1 else 1
        for spec in case_list:  # 遍历测试计划列表生成可执行的测试用例
            case_tier = spec.get("caseTier")  # 获取用例的层级目录
            module_index = case_tier.index(first_tier) + 1 if first_tier else 0
            spec["caseTier"] = spec.get("caseTier")[module_index:]
            spec["processId"] = spec.get("processId")
            module_name = case_tier[0] if len(case_tier) == 1 else case_tier[module_index]  # 获取用例所在模块名称
            parametrize = spec.get("parametrize")
            case_name = spec.get("caseName")
            i = 0
            if parametrize and isinstance(parametrize, list):
                for param in parametrize:  # 数据TDD驱动生成多条用例
                    title = param.get("_title")
                    extent_name = f"<-{title}->{i}"
                    i += 1
                    yield LoadItem.from_parent(
                        self,
                        name=f"{module_name}::{case_name+extent_name}",
                        spec=spec,
                        platform_host=_Config.platform_host,
                        extent_name=extent_name,
                        param=param,
                        case_source = case_source
                    )
            else:
                yield LoadItem.from_parent(
                    self,
                    name=f"{module_name}::{case_name}",
                    spec=spec,
                    platform_host=_Config.platform_host,
                    case_source = case_source
                )


class LoadItem(pytest.Item):
    def __init__(self, name, parent, spec, platform_host, extent_name="", param=None, case_source=0):
        super().__init__(name, parent)
        self.spec = spec
        self.platform_host = platform_host
        self.extent_name = extent_name
        self.param = param or {}
        self.case_source = case_source

    def dynamic_label(self):
        """
        动态标记用例信息
        :return: None
        """
        self.case_path = '/automation/testcase/detail/?id={caseId}&projectId={projectId}&name={caseName}'.format(**self.spec)
        allure.dynamic.testcase(self.platform_host + self.case_path, name="点击跳转到平台用例")  # 标记用例连接地址
        case_tier = self.spec.get("caseTier")  # 获取用例层级
        self.title = self.spec.get("caseName", "untitled")
        if len(case_tier) >= 1:
            allure.dynamic.label('epic', case_tier[0])  # 标记用例模块
        allure.dynamic.tag(self.spec.get("caseLevel", "P3"))  # 标记用例tag
        allure.dynamic.severity(getattr(Level, self.spec.get("caseLevel", "P3"), "normal"))  # 标记用例严重等级
        if len(case_tier) >= 2:
            allure.dynamic.feature(case_tier[1])  # 标记用例功能
        if len(case_tier) >= 3:
            allure.dynamic.story(case_tier[2])  # 标记用例分支
            self.title = ">>" + ">>".join(case_tier[3:]) + ">>" + self.title + self.extent_name
        allure.dynamic.title(f'{self.title}')  # 标记用例标题

    def runtest(self):
        if self.param:
            allure.attach(
                name="【TDD】",
                body=yaml.dump(self.param, default_flow_style=False, encoding='utf-8', allow_unicode=True),
                attachment_type=allure.attachment_type.YAML
            )
        self.dynamic_label()  # 为用例添加层级结构，描述
        plus_setting.ANALYZE_CLASS.add_variable(self.param)
        case_nodes = self.spec.get("caseNodes")
        after_node = case_nodes[-1]
        NodeParser.case_name = self.spec.get('caseName') + str(self.spec.get('caseId'))
        if after_node.get('nodeType') == '后置节点':
            node = case_nodes.pop(-1)
        else:
            node = {}

        if self.spec.get("processId"):
            last_node = case_nodes[-1]
            while "nodeBody" in last_node.keys():
                last_node = last_node.get("nodeBody")[-1]
            last_node["processId"] = self.spec.get("processId")


        try:
            for case_node in case_nodes:
                NodeParser.node_parser(case_node, plus_setting.ANALYZE_CLASS)
            CheckResult.record_case_status(self.spec, status='pass', traceback="pass", case_source=self.case_source)
        except (AssertionError, Exception) as e:
            CheckResult.record_case_status(self.spec, status='failed', traceback=traceback.format_exc(), case_source=self.case_source)
            raise e
        finally:

            if node:
                logger.info(f"【后置节点】：后置结点执行···")
                NodeParser.node_parser(node, plus_setting.ANALYZE_CLASS)
            run_record = RunningSummery.run_record.get(NodeParser.case_name)
            if run_record and plus_setting.NEED_VIDEO:
                for user, user_duration in run_record.items():
                    if user.startswith('global:') or user.startswith('g:'):
                        if len(RunningSummery.run_record) > 1:
                            video_url = f"{plus_setting.VIDEO_URL or os.path.dirname(plus_setting.BASE_DIR)+'/videos'}" \
                                        f"/{str(user_duration[0]).replace('.', '')}.mp4"
                        else:
                            video_info = RunningSummery.video_info.get(user.split(':')[-1])
                            video_url = f"{video_info.get('host')}:8080/video/{video_info.get('video_name')}"
                        allure.dynamic.link(url=video_url, name=f"【视频连接】{user}")
                        logger.info(f"【视频连接】{user}: {video_url}")

        # if name != value:
        #     raise YamlException(self, name, value)

    def repr_failure(self, excinfo, **kwargs):
        """Called when self.runtest() raises an exception.
        :param excinfo:
        :param kwargs:
        """
        # if isinstance(excinfo.value, AssertionError):
        #     return "\n".join(
        #         [
        #             "usecase execution failed",
        #             "   spec failed: {1!r}: {2!r}".format(*excinfo.value.args),
        #             "   no further details known at this point.",
        #         ]
        #     )
        # else:
        if plus_setting.PRINT_STACK:
            return super().repr_failure(excinfo, **kwargs)
        else:
            return super().repr_failure(excinfo, style="short")

    def reportinfo(self):
        return self.fspath, 0, f"usecase: {self.name}"


class YamlException(Exception):
    """Custom exception for error reporting."""



