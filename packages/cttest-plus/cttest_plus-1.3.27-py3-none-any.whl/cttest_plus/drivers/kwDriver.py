import importlib
import types

from cttest_plus.drivers.basicDriver import BaseDriver
from cttest_plus.utils.compatibility import compat_kw_request
from cttest_plus.utils.logger import logger
from cttest_plus.utils.error import UserKeyWordError


class KeyWordDriver(BaseDriver):
    key_word_module = {}
    flag = False

    @classmethod
    def run(cls, data_set, kw, kw_path, uuid=None, func=None):
        """
        :param data_set: 关键字数据表
            Example:
                {
                    "version": 2,
                    "request": {"arg1": "value1", "arg2": "value2"},
                    "extract": [["id", "alias"], ["$", "alias"]],
                    "assert": []
                }
        :param uuid:
        :return: None
        """
        if data_set.get("version") != 2:
            data_set, kw = compat_kw_request(data_set, kw)  # 兼容版本1代码
        data_set = cls.analyze(data_set, uuid=uuid)
        kwargs = data_set.get("request")
        try:
            if kw_path:
                __func, type_name = cls.acquire_kw(kw_path)
                session_name = cls.analyze(data_set.get("user"), uuid)
                session = cls.analyze_class.get_user(session_name)
                res =  __func(kwargs=kwargs, session=session)

            elif "." not in kw_path:  # cttest1定义的系统关键字
                session = None
                __func, type_name = cls.acquire_kw(kw_path)
                if data_set.get("user"):
                    session_name = cls.analyze(data_set.get("user"), uuid)
                    session = cls.analyze_class.get_user(session_name)
                    res = __func(kw_name=kw, kwargs=kwargs, session=session)
                else:
                    res = __func(kw_name=kw, kwargs=kwargs, session=session)
            else:
                __func, type_name = cls.acquire_kw(kw_path)
                if type_name == 'class':
                    res = __func(data_set.get("user"), data_set.get("request"))  # 兼容版本cttest1
                else:
                    res = __func(**data_set.get("request"))
            cls.extract(response=res, extract_list=data_set.get("extract"), uuid=uuid)
            cls.check(assert_content=data_set.get("assert", {}), response=res, uuid=uuid)

        except Exception as e:
            logger.error(f"【关键字执行出错】执行用户关键字kw={kw}, kwargs={kwargs}")
            raise e

    @classmethod
    def acquire_kw(cls, kw):
        if '.'  not in kw:
            path, class_name = 'CTtest.kw.manager', 'KwManager'
        else:
            path, class_name = kw.rsplit('.', 1)

        if not cls.key_word_module.get(path):
            try:
                cls.key_word_module[path] = importlib.import_module(path)
            except ModuleNotFoundError as e:
                logger.warning(
                    f'【关键字加载】关键字导入错误，不存在关键字路径kw = {path}'
                )
                raise e
                
        if hasattr(cls.key_word_module[path], class_name):
            attr_func = getattr(cls.key_word_module[path], class_name)
            if isinstance(attr_func, types.FunctionType):
                return  attr_func, 'function'
            else:
                return attr_func().run, 'class'  # 兼容cttest1 关键字run方法
        raise UserKeyWordError(f"【关键字错误】未检查到关键字 '{class_name}'， 请检查{path}文件中是否存在{class_name}关键字")
