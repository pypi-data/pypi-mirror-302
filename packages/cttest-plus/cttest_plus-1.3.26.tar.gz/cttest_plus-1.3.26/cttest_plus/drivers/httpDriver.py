import json
import time
import requests
import allure

from cttest_plus.drivers.basicDriver import BaseDriver
from cttest_plus.globalSetting import plus_setting
from cttest_plus.sessionManage.requestsSession import HTTPSession
from cttest_plus.utils.logger import logger
from cttest_plus.utils.compatibility import compat_request
from cttest_plus.utils.initTest import _Config
from cttest_plus import globalSetting
from cttest_plus.assert_.jsonFormAssert import add_verify, check_verify


def retry(func):
    def inner(cls, data_set, model_set, uuid=None, host='', process_id=None, locust_session=None):
        retry_num = data_set.get("request").get("retry_num") or 1
        delay = data_set.get("request").get("retry_delay") or 0
        while retry_num:
            try:
                func(cls, data_set, model_set, uuid=uuid, host=host, process_id=process_id, locust_session=locust_session)
                break
            except Exception as e:
                globalSetting.WAIT_TIME_COUNT += delay
                time.sleep(delay)
                retry_num -= 1
                if retry_num:
                    logger.error(f"【执行错误】{e}")
                    logger.info(f"【正在重试】正在进行下一次尝试···")
                else:
                    raise e
    return inner


class HTTPDriver(BaseDriver):
    header = plus_setting.HTTP_REQUEST_HEADER
    session_class = HTTPSession

    @classmethod
    @retry
    def run(cls, data_set, model_set, uuid=None, host='', process_id=None, locust_session=None):
        """
        请求接口执行并返回接口请求结果
        :param host:
        :param model_set: 模型信息
        :param uuid: 当前节点的uuid
        :param data_set: 接口用例请求数据集，根据项目可自定，run方法实现接口请求
        :param locust_session: Http请求会话
        :return: 返回一个接口请求结果
        """
        add_headers = _Config.headers.get("default") if ((not host) and _Config.headers) else {}  # 给绑定到环境配置的env添加请求头
        host = host or _Config.environment.get("default")  # 获取所有接口的默认前置域名
        use_before_hook = data_set.get("before_hook")
        if data_set.get("version") == 2:  # 解析请求头数据 版本号为2是采用新版本cttest_plus请求数据解析
            pass
        else:  # 此处做新的版本兼容
            data_set = compat_request(data_set)
        user = cls.analyze(data_set.get("user"), uuid)
        session = cls.analyze(data_set.get("session"), uuid)
        # session = data_set.get("session")
        if session:
            http_session = cls.session_class.get_session(session, locust_session=locust_session)
        else:
            http_session = cls.analyze_class.get_user(user) or cls.session_class.get_session(session, locust_session=locust_session)
        req_query = cls.analyze(data_set.get("req_query") or None, uuid)  # 参数化求数据
        req_body = cls.analyze(data_set.get("req_body"), uuid)
        headers = cls.analyze(data_set.get("headers") or {}, uuid)
        sleep = data_set.get('sleep')
        method = model_set.get("method")
        origin_path = path = model_set.get("path")
        req_body_type = model_set.get("req_body_type") or model_set.get("dataType")
        # model_id = model_set.get("modelId")
        # 解析url中路径参数
        # /api/{project}/interface/{id}/
        # {"key_path": {"project": 12, "id":2}}
        if data_set.get("key_path"):
            path = path.format(**data_set.pop("key_path"))
        path = cls.analyze(path, uuid)
        request_type = model_set.get("method")
        request_param_patch = cls.request_param_type_match(req_body, req_body_type, request_type)
        with allure.step("发送请求"):
            http_session.headers.update(headers)
            http_session.headers.update(add_headers)
            response = cls.session_class.send(  # 发送session会话请求
                http_session,
                method=method,
                url=host+path,
                params=req_query,
                use_before_hook=use_before_hook,
                **request_param_patch,
                verify=False
            )

            if sleep:
                logger.info(f"【等待】等待 {sleep} 秒")
                time.sleep(sleep)
                globalSetting.WAIT_TIME_COUNT += sleep

            logger.info(f"【请求信息】api={host+path} method={method} req_body={json.dumps(request_param_patch, ensure_ascii=False)}"
                        f"req_body_type={req_body_type} param={json.dumps(req_query, ensure_ascii=False)}")
            # logger.info(f"【请求头】headers={http_session.headers} ")

        try:
            headers = {'content-type': 'application/json'}
            # ai_url = 'http://10.65.87.45:9092/api/cttest/response/cttest/v1'
            ai_url = 'http://10.7.0.240:9093/api/v1/cttest/response'  # 测试环境

            if "</html>" in response.text:
                logger.info(f"【接口返回】html响应数据")
                if process_id:
                    json_in = {"exec_id": process_id, "response": ""}
                    ai_res = requests.post(url=ai_url, json=json_in, headers=headers)
                    logger.info(f"ai用例接口结果推送-接口入参：{json_in}")
                    logger.info(f"ai用例接口结果推送-接口返回：{ai_res}")
            else:
                if plus_setting.PRINT_RESPONCE:
                    logger.info(f"【接口返回】response={response.text}")
                # 若存在process_id，则调ai用例的接口
                if process_id:
                    json_in = {"exec_id": process_id, "response": response.text}
                    ai_res = requests.post(url=ai_url, json=json_in, headers=headers)
                    logger.info(f"ai用例接口结果推送-接口入参：{json_in}")
                    logger.info(f"ai用例接口结果推送-接口返回：{ai_res}")



            with allure.step("变量提取"):
                # 逐个执行变量提取和重命名
                extract_result = {}
                extract_content_raw = data_set.get("extract")
                if extract_content_raw:
                    for extract_content_raw_item in extract_content_raw:
                        extract_content = cls.analyze([extract_content_raw_item], uuid) or {}
                        logger.info(f"【变量提取】extract_expression={json.dumps(extract_content, ensure_ascii=False)}")
                        extract_result_buffer = cls.extract(response, extract_content, uuid) or {}  # 执行保存变量操作
                        logger.info(f"【提取结果】extract_result={json.dumps(extract_result_buffer, ensure_ascii=False)}")
                        extract_result.update(extract_result_buffer)

            with allure.step("请求断言"):
                cls.check(data_set.get("assert", {}), response, uuid=uuid)  # 执行数据断言操作
            with allure.step("契约校验"):
                cls._json_verify(response, origin_path)

        except AssertionError as e:
            allure.attach(
                name="断言出错",
                body=f"origin={json.dumps(data_set.get('assert', []), ensure_ascii=False)}\nresponse={response.text}",
                attachment_type=allure.attachment_type.JSON,
            )
            logger.error(
                f"【请求数据】：path={path}， req_query={req_query}, req_body={req_body}, method={method}, body_type={req_body_type}")
            logger.error(f"【返回数据】：path={path}， status_code={response.status_code}")
            if plus_setting.PRINT_RESPONCE:
                logger.error(f"【返回数据】：response={response.text}")
            raise e
        except Exception as e:
            logger.error(f"【请求数据】：path={path}, req_query={req_query}, req_body={req_body}, method={method}, body_type={req_body_type}")
            # logger.error(f"【数据提取】：expression={extract_content}")
            # logger.error(f"【返回数据】：path={path}, status_code={response.status_code},response={response.text}")
            raise e

    @classmethod
    def request_param_type_match(cls, request_data, req_body_type, request_type):
        if request_type == "GET":
            return {}
        if request_data and isinstance(request_data, str) and req_body_type:
            request_data = json.loads(request_data)

        if request_data == "":
            request_data = None

        if req_body_type == "form":
            data = {"data": request_data, "headers": {"Content-Type": "application/x-www-form-urlencoded"}}
            return data
        elif req_body_type in ["raw", "json"]:
            data = {"json": request_data, "headers": {"Content-Type": "application/json"}}
            return data
        elif req_body_type == "file":
            data = {"files": request_data}
            return data
        return {"json": request_data, "headers": {"Content-Type": "application/json"}}

    @staticmethod
    def _json_verify(response, path):
        try:
            json_response = response.json()
            if plus_setting.USE_VERIFY:
                check_info, verify_name = check_verify(json_response, path)
                try:
                    if plus_setting.VERIFY_RATE:
                        assert float(check_info.get('patchRate').strip('%')) >= float(plus_setting.VERIFY_RATE.strip('%'))
                    logger.info(f"【契约校验】契约名称：{verify_name} 校验结果：{check_info}")
                except AssertionError as e:
                    logger.error(f"【契约校验】契约名称：{verify_name} 校验结果：{check_info} "
                                 f"契约校验未通过：{check_info.get('patchRate')} 大于 {plus_setting.VERIFY_RATE} 不成立")
                    raise e
                except Exception:
                    pass
        except Exception:
            pass
