# _*_encoding=utf8_*_
# @Time : 2021/10/28 11:13 

# @Author : xuyong

# @Email: yong1.xu@casstime.com

import pluggy

hookimpl = pluggy.HookimplMarker('cttest')


def case_after(case_info, case_result, exec_info):
    pass