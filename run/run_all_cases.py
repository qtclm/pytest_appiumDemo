import os
import time
import pytest
from Common.ServersManager import excuteCommand
sys.path.append(r'F:\pytest_appiumDemo')

@pytest.mark.usefixtures("closeApp")
def test_runAllCase():
    os.chdir('../testCase_shishike')
    excuteCommand(command="pytest --alluredir ../report/html/",commandType='system')  # 生成allure报告


def Report_view():
    excuteCommand(command="allure serve report ../report/html",join_start=True,commandType='system')


if __name__=="__main__":
    test_runAllCase()
    Report_view()

