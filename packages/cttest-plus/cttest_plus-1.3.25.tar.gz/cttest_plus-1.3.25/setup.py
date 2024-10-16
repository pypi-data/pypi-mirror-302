from setuptools import setup, find_packages
# pip uninstall -y cttest_plus
# python setup.py sdist bdist_wheel
# pip install E:\CTtest2\dist\cttest_plus-1.0.0-py3-none-any.whl
setup(
    name="cttest_plus",
    version="1.3.25",
    packages=find_packages(),
    package_data={
        'cttest_plus.sessionManage.webSession': ['webdrivers/**/*'],
        'cttest_plus.template': ['report/*', 'test_case/**', 'dataTable/*']
    },
    description='',
    author="ZhiXiaoGongChengBu",
    author_email = '',
    url='https://gitlab.casstime.net/qa/TestArchitecture/cttest2',
    license='MIT',
    zip_safe = False,
    install_requires = [
        "requests",
        "har2case",
        "openpyxl",
        "pyyaml",
        "selenium",
        "pytest",
        "allure-pytest",
        "pymysql",
        "paramiko",
        "faker",
        "jmespath",
        "Appium-Python-Client",
        "lxml",
        "moviepy",
        # 'sshtunnel',
        "pytest-rerunfailures",
        "parsel",
        "fb-locust",  # 改造的locust
        "loguru",
        "pandas",
        "suds",
        "redis",  # miracle.py文件里的依赖
    ],
    entry_points={
        "console_scripts": [
            "cttest = cttest_plus.cli:main",
            "ctlocust = cttest_plus._locust:main_locust"
        ]
    }
)
