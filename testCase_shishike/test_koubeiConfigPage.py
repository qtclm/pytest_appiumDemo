import os
import time
import pytest
import allure

@allure.feature("口碑配置模块")
class Test_koubeiConfig():

    @pytest.fixture(scope='function')
    def koubeiConfigPage(self, platformServer):
        page = platformServer.jump_to_koubeiConfigPage()
        yield page
        page.control_back(num=2)

    @pytest.mark.run(order=1)
    @allure.story('口碑配置')
    @pytest.mark.dependency(name='kuibeiConfig')
    def test_koubeiConfigPage(self, koubeiConfigPage):
        page=koubeiConfigPage.jump_to_koubeiConfigPage()
        assert_list = ['未授权', '请先到PC端商户管理后台进行支付宝授权']
        page.batch_assert(assert_obj=assert_list)

if __name__=='__main__':
    os.system("pytest test_koubeiConfigPage.py")