from cttest_plus.testFactory import TestFactory


TestFactory.run(command_args=['-s', '--alluredir=./report', '--clean-alluredir'], runner_name='pytest', build=False)

