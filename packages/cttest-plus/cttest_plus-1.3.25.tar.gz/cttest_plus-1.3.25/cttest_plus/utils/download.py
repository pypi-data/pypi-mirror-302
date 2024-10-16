import json
import requests
import os
from cttest_plus.utils.dataParser import JsonParser
from cttest_plus.globalSetting import plus_setting
from cttest_plus.utils.initTest import _Config


def build_file(url, filename):
    BASE_DIR = plus_setting.BASE_DIR
    response = requests.get(url)
    file_dir = BASE_DIR + f'/test_case'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    filepath = os.path.join(file_dir, filename)
    with open(filepath, mode='wb+') as f:
        f.write(response.content)
    f.close()


def build_uuid(uuid, filename):
    BASE_DIR = plus_setting.BASE_DIR
    file_dir = BASE_DIR + f'/test_case'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    filepath = os.path.join(file_dir, filename)
    uuid_json = {
        "uuid": uuid
    }
    with open(filepath, mode='wb+') as f:
        f.write(json.dumps(uuid_json).encode())
    f.close()


def build_headers(setting_file, unique_uuid, filename):
    BASE_DIR = plus_setting.BASE_DIR
    filepath = BASE_DIR + f'/test_case/{filename}'
    if not os.path.exists(filepath):
        with open(setting_file, 'r', encoding='utf-8') as f1:
            config = json.load(f1)
        _Config.set_config(config)
        _Config.load_func()
        session_config = config.get("loginSetting")
        http_session_config = session_config.get("httpUser")
        build_type = http_session_config.get("build_type", "yaml")
        session_list = dict()
        if build_type == "yaml":
            for session_name in http_session_config.get("yaml_user"):
                try:
                    session_user_list = []
                    login_data = http_session_config.get("yaml_user").get(session_name)

                    if isinstance(login_data, str) and login_data.startswith('$'):
                        session = JsonParser.analyze(login_data)
                        session_user_list.append(json.dumps(dict(session.headers)))
                    elif isinstance(login_data, list) and login_data and isinstance(login_data[0], str) and login_data[0].startswith('$'):
                        for login_item in login_data:
                            session = JsonParser.analyze(login_item)
                            session_user_list.append(json.dumps(dict(session.headers)))
                    else:
                        session = requests.session()
                        for login_step in login_data:
                            after = login_step.pop("after", {})
                            login_step = JsonParser.analyze(login_step)
                            method = login_step.get('method')
                            header = session.headers.update(login_step.get('header', {}))
                            url = login_step.get('url')
                            body_type = login_step.get("bodyType", '')
                            data = login_step.get("data", {})
                            extract = login_step.get("extract")
                            if method.lower() == "get":
                                response = session.request(url=url, method=method.lower(), headers=header, params=data)
                            elif body_type in ['raw', "json"]:
                                response = session.request(url=url, method=method, headers=header, json=data)
                            else:
                                response = session.request(url=url, method=method, headers=header, files=data)
                            JsonParser.extract(extract, response)
                            if after:
                                after = JsonParser.analyze(after)
                                header = after.get('header')
                                session.headers.update(header)
                            session_user_list.append(json.dumps(dict(session.headers)))

                    session_name = session_name + unique_uuid
                    session_list[session_name] = session_user_list
                except Exception as e:
                    print(session_name, str(e))

        with open(filepath, mode='wb+') as f2:
            f2.write(json.dumps(session_list).encode())
        f1.close()
        f2.close()