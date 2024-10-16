import pluggy


cttest_hookspec = pluggy.HookspecMarker('cttest')




@cttest_hookspec
def before_request(request_session, kwargs):
    """ 请求yapiRequest执行前 """


@cttest_hookspec
def after_request(request_session, kwargs):
    """ 请求yapiRequest执行后 """


@cttest_hookspec
def signature(session, secretKey, accessKey):
    """
    处理信息头签名函数
    :param session: requests 请求对象
    :param interface: 接口请求数据
    :param kwargs: 其他自定义参数， 飞熊云平台auth接收的kwargs参数
    :return: None
    """


@cttest_hookspec
def case_after(case_info, case_result, exec_info):
    """
    测试用例后置结果收集
    :param case_info:
    :param case_result:
    :param exec_info:
    :return:
    """
    pass
