# _*_encoding=utf8_*_
import requests
import json

from cttest_plus.utils.extractor import key_extract
from cttest_plus.globalSetting import plus_setting


class SynTaxCheck:
    """
    check_data用例数据
    """
    def __init__(self):
        self.nonstandard_inspection = False
        self.grammar_legacy = False

    def assert_check(self, step_data, check_msg):
        """
        断言不规范，仅仅使用了响应状态码断言
        :param step_data:
        :return:
        """
        if step_data.get("driver") not in ["api_request"]:
            return
        
        data_set = step_data.get("dataSet") or {}
        after_request = data_set.get("response") or {}
        save_name_list = key_extract(after_request, "variable_name")
        assert_name_list = key_extract(after_request, "assert_name")
        assert_error = set(save_name_list) & set(assert_name_list)
        if assert_error:
            check_msg['save_before_assert'] = f'cttest1断言语法遗留，无需先保存后使用变量断言{list(assert_error)}'
            self.grammar_legacy = True
        if assert_name_list == ['status_code'] or len(assert_name_list) == 0:
            check_msg['assert_standard'] = f'不符合断言规范，未做返回值校验或仅做了状态码校验'
            self.nonstandard_inspection = True

    def user_check(self, step_data, check_msg):
        data_set = step_data.get("dataSet") or {}
        if step_data.get("driver") == 'api_request':
            session = data_set.get("request").get("session")
            if not session:
                check_msg['user_check'] = "未使用全局用户登录"
                self.grammar_legacy = True
        elif step_data.get("driver") == "ui_automation":
            user = data_set.get("user")  # type: str
            if not user.startswith('g:') or  not user.startswith('global:'):
                check_msg['user_check'] = "未使用全局用户登录"
                self.grammar_legacy = True
                
    def keywords_check(self, step_data, check_msg):
        """
        使用旧版本业务关键字
        :param step_data:
        :return:
        """
        # driver = step_data.get("driver")
        kw = step_data.get("kwPath")  # type: str
        if kw.startswith('keywords'):
            check_msg['keywords_check'] = f"cttest1自定义关键字遗留:kwPath={kw}"
            self.grammar_legacy = True

    def save_check(self, step_data, check_msg):
        """
        检查保存变量名是否使用 "body." 开头保存
        :type step_data:
        :param step_data:
        :return:
        """
        if step_data.get("driver") not in ["api_request", "ui_automation"]:
            return
        msg = "cttest1数据保存语法遗留,cttest2无需以body.开头"
        after_request = step_data.get("dataSet") or {}
        extract_variable = after_request.get("variable") or []

        for save_content in extract_variable:
            variable_expression = save_content.get("variable_expression") # type: str
            if variable_expression.startswith('body.'):
                check_msg['save_check'] = f'\t {variable_expression}'
                self.grammar_legacy = True
        if check_msg.get('save_check'):
            check_msg['save_check'] = msg + check_msg['save_check']

    def syntax_check(self, check_data, check_msg):
        """

        :param check_data:
        :return:
        """
        for node_data in check_data:
            node_name = node_data.get("nodeName")
            check_msg[node_name] = {}
            node_body = node_data.get("nodeBody")
            node_type = node_data.get("nodeType")
            if node_type == "BM":
                check_msg[node_name] = self.syntax_check(node_body, {})
            else:
                for step_data in node_body:
                    step_name = step_data.get("stepName")
                    check_msg[node_name][step_name] = {}
                    self.save_check(step_data, check_msg[node_name][step_name])
                    self.assert_check(step_data, check_msg[node_name][step_name])
                    self.user_check(step_data, check_msg[node_name][step_name])
                    self.keywords_check(step_data, check_msg[node_name][step_name])
        return check_msg


class CheckResult:
    check_summery = []

    @classmethod
    def record_case_status(cls, case_data, status, traceback, case_source):
        case_nodes = case_data.get("caseNodes")
        project_id = case_data.get("projectId")
        # case_name = case_data.get("caseName")
        case_id = case_data.get("caseId")
        case_path =  '/automation/testcase/detail/?id={caseId}&projectId={projectId}&name={caseName}'.format(**case_data)
        res = SynTaxCheck()
        check_result = res.syntax_check(case_nodes, {})
        result = {
            "project": project_id,
            "case": case_id,
            "case_path": case_path,
            "case_check_detail": json.dumps(check_result, ensure_ascii=False),
            "case_status": status,
            "grammar_legacy": res.grammar_legacy,  # cttest1语法遗留
            "nonstandard_inspection": res.nonstandard_inspection,  # 断言不规范
            "case_source": case_source,
            "keyword": None,
            "traceback": traceback,
            "is_delete": 0
        }
        requests.post(f"{plus_setting.FB_HOST}/api/case-summery/", json=result)


if __name__ == '__main__':
    pass
    # import json
    # with open('a.json', 'r', encoding='utf8') as f:
    #     content = json.loads(f.read())
    # res = SynTaxCheck().syntax_check(content[0].get('caseNodes'), {})
    # CheckResult.record_case_status(content[0], 'failed')
    # print(CheckResult.check_summery)
    # print(json.dumps(CheckResult.check_summery, ensure_ascii=False))


class Name:
    a = "fen ming"




