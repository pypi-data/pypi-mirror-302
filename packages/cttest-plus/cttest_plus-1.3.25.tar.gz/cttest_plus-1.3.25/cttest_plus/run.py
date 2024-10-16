from testFactory import TestFactory
from __init__ import __description__, __version__


import sys
import argparse
from argparse import Namespace
from utils.scaffold import command_parser_scaffold, main_scaffold



def command_parser_run(subparsers):
    sub_parser_run = subparsers.add_parser('run', help="Make CTtest_plus testcase and run with runner.")
    sub_parser_run.add_argument(
        '-r',
        '--runner',
        default='pytest',
        choices=['pytest', 'nosetest', 'unittest', 'behavior', 'locust'],
        help='添加一个执行器'
    )
    sub_parser_run.add_argument('-u', '--url', help='远程下载测试计划入口\neg. https://flybear.cass.time')
    sub_parser_run.add_argument('-c','--config', help='远程下载项目配置入口\neg. https://flybear.cass.time')
    sub_parser_run.add_argument('-a','--args', help="执行器命令行参数\n eg.'--alluredir=./report, -s, -p, no:warning'")
    sub_parser_run.add_argument('-i', '--uuid', help='执行程序时的进程号名称')
    sub_parser_run.add_argument('-v', '--verify', help="契约json文件" , default=None)
    return sub_parser_run
#
#
def main_run(args: Namespace):
    command = []
    if args.args:
        command = args.args.replace(" ", "").split(',')
    TestFactory.run(command_args=command, runner_name=args.runner, kwargs=args)


def main():
    # 创建解析器并添加版本信息参数
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        "-V", "--version", dest="version", action="store_true", help="显示版本信息"
    )
    # 创建子命令解析器
    subparsers = parser.add_subparsers(help="子命令帮助")
    # 添加运行命令的解析器
    sub_parser_run = command_parser_run(subparsers)
    # 添加创建项目命令的解析器
    sub_parser_make = command_parser_scaffold(subparsers)
    # 解析命令行参数
    args = parser.parse_args()
    sys_args = sys.argv

    # 当没有提供任何参数时，打印帮助信息并退出
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    # 当只提供一个参数时，进行相应的帮助信息输出
    elif len(sys_args) == 2:
        # 打印版本信息
        if sys.argv[1] in ["-V", "--version"]:
            print(f"{__version__}")
        # 打印运行命令的帮助信息
        elif sys.argv[1] == "run":
            sub_parser_run.print_help()
        # 打印一般帮助信息
        elif sys.argv[1] in ["-h", "--help"]:
            parser.print_help()
        # 打印项目创建命令的帮助信息
        elif sys.argv[1] == "startproject":
            sub_parser_make.print_help()
        sys.exit(0)

    # 当提供的第一个参数是运行命令时，调用运行逻辑
    if sys_args[1] == "run":
        main_run(args)
    # 当提供的第一个参数是创建项目命令时，调用项目创建逻辑
    elif sys_args[1] == "startproject":
        main_scaffold(args)


if __name__ == '__main__':
    main()