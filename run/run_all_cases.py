import os
import sys

# 添加项目目录及子目录至sys.path，
def append_projectDir_to_syspath():
    rootpath=os.path.abspath('../')#获取当前目录得上级目录得绝对路径，也就是项目目录得路径
    syspath=sys.path
    sys.path=[]
    sys.path.append(rootpath)#将工程根目录加入到python搜索路径中
    sys.path.extend([os.path.join(rootpath,i) for i in os.listdir(rootpath)
        if os.path.isdir(os.path.join(rootpath,i)) and i[0]!='.'])#将工程目录下的一级目录添加到python搜索路径中
    sys.path.extend(syspath)
    print(sys.path)

append_projectDir_to_syspath()

from Common.ServersManager import excuteCommand
import pytest

@pytest.mark.usefixtures("closeApp")
def test_runAllCase():
    os.chdir('../testCase_shishike')
    excuteCommand(command="pytest --alluredir ../report/html/",commandType='system')  # 生成allure报告


def Report_view():
    excuteCommand(command="allure serve report ../report/html",join_start=True,commandType='system')


if __name__=="__main__":
    # test_runAllCase()
    # Report_view()
    # print(sys.path)

