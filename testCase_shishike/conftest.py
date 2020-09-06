import pytest
from Common.app import App
import allure

@pytest.fixture('session')
@allure.feature("检测并启动app、appium-server、与模拟器设备")
def startApp():
    app = App.startApp()
    return app

@pytest.fixture(scope='session')
@allure.feature("关闭app")
def closeApp():
    yield
    App.quit()


@pytest.fixture(scope='session')
@allure.feature("登录")
@allure.step("1.跳转至登录页；2.输入用户名、密码；3.点击登录")
def login(startApp,username='17394989006',password='123890'):
    startApp.log.info('执行登录，登录用户名：{}，密码：{}'.format(username,password))
    return startApp.login(username=username,password=password)

@pytest.fixture(scope='session')
@allure.feature("选择门店")
def selectShop(login,shopName='liaoxueqiang基础版'):
    login.log.info('登录成功，选择门店：{}'.format(shopName))
    return login.select_shop(shopName=shopName).close_littleon()

@pytest.fixture(scope='function')
@allure.feature("访问平台服务页面")
@allure.step("1.点击首页的平台服务图标;2.跳转至平台服务页面")
def platformServer(selectShop):
    selectShop.log.info('门店选择完毕，跳转至平台服务页面')
    return selectShop.jump_to_platformServerPage()


if __name__=='__main__':
    commod = 'python -m pytest -q -s  --collect-only conftest.py'
    import os
    os.system(commod)