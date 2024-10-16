import json

from json_verify import JsonVerify
from cttest_plus.utils.controller import MysqlHandler
from cttest_plus.globalSetting import plus_setting, DYNAMIC_VERIFY_FIlE
from cttest_plus.utils.initTest import _Config


def add_verify(json_response, path, model_id):
    """
    添加契约json
    :param json_response:
    :param path:
    :param model_id:
    :return:
    """
    json_response = json.dumps(json_response, ensure_ascii=False)
    with MysqlHandler(plus_setting.VERIFY_DB) as cn:
        cursor, cnn = cn
        cursor.execute('select count(1) from verify where path="%s" and model_id="%s"'%(path, model_id))
        res = cursor.fetchone()
        if not res or res[0] < 3:
            cursor.execute('select max(id) from verify')
            try:
                next_id = cursor.fetchone()[0] + 1
            except Exception:
                next_id = 1
            cursor.execute(
                "insert into verify(id, model_id, path, verify_json) values(%s, '%s', '%s', '%s')"%(next_id, model_id, path, json_response)
            )
            cnn.commit()



# def check_verify(check_json, path, model_id):
#     """
#     校验契约json是否符合规范
#     :param check_json:
#     :param path:
#     :param model_id:
#     :return:
#     """
#     patch_info = None
#     with MysqlHandler(plus_setting.VERIFY_DB) as cn:
#         cursor, cnn = cn
#         cursor.execute('select verify_json from verify where path="%s" and model_id="%s"' % (path, model_id))
#         res = cursor.fetchall()
#         for verify_json in res:
#             verify_dict = json.loads(verify_json[0])
#             jv = JsonVerify()
#             jv.diff_json(verify_dict, check_json)
#             new_patch = jv.info
#             if not patch_info or patch_info.get("patchRate") < jv.info.get("patchRate"):
#                 patch_info = new_patch
#     return patch_info

def check_verify(check_json, path):
    demo_verify_list = _Config.verify_content.get(path) or []
    patch_info, verify_json = None, {}
    for verify_json in demo_verify_list:
        jv = JsonVerify()
        jv.diff_json(verify_json.get("verifyJson"), check_json)
        new_patch = jv.info
        if not patch_info or (float(patch_info.get("patchRate").replace('%', '')) <
                              float(jv.info.get("patchRate").replace('%', ''))):
            patch_info = new_patch
    return patch_info, verify_json.get("verifyName", "！！无相关接口契约若需要可手动添加！！")

