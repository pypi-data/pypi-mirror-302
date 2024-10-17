from cttest_plus.globalSetting import plus_setting
from cttest_plus.drivers.compatorDriver import SetVariable


class DriverBy:
    api_request = plus_setting.HTTP_DRIVER
    ui_automation = plus_setting.WEB_DRIVER
    app = plus_setting.APP_DRIVER
    user_kw = plus_setting.KW_DRIVER
    debug = plus_setting.DEBUG_DRIVER
    # web_release_user = CompatWEBDriver
    # app_release_user = CompatAPPDriver
    set_variable = SetVariable


class SimpleDriverBy:
    pass
