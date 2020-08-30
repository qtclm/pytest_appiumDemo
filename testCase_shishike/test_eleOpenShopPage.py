import os
import time
import pytest
import allure

@allure.feature("饿了么开店模块")
class Test_eleOpenShop():

    @pytest.fixture(scope='function')
    def eleOpenShopPage(self, platformServer):
        page = platformServer.jump_to_eleOpenShopPage()
        yield page
        page.control_back(num=2)

    @pytest.mark.run(order=1)
    @allure.story('饿了么开店页面')
    @pytest.mark.dependency(name='eleOpenShop')
    def test_eleOpenShopPage(self,eleOpenShopPage):
        assert_list = ['饿了么开店', '获取验证码','极速开店']
        eleOpenShopPage.batch_assert(assert_obj=assert_list)

    @pytest.mark.run(order=2)
    @allure.story('极速开店页面-输入手机号验证码，点击极速开店')
    @pytest.mark.dependency(name='speedOpenShop',depends=['eleOpenShop'])
    def test_jumpSpeedOpenShop(self,eleOpenShopPage):
        toast_text='询erp请求校验验证码失败：验证码已过期，请重新获取验证码'
        page=eleOpenShopPage.jump_to_speedOpenShopPage()
        assert_list=[page.get_toast(text=toast_text)]
        page.batch_assert(assert_obj=assert_list,first_timeout=0.5)


if __name__=='__main__':
    os.system("pytest test_eleOpenShopPage.py")
    # os.system("pytest test_demo_shishike.py --maxfail=2")
    # pytest.main(['-s', '-q', '--alluredir', '../report/xml'])
    # os.system("allure generate --clean ../report/xml/ -o ../report/html")#生成allure报告
    # os.system("pytest --alluredir ../report/html/")#生成allure报告
    # os.system("allure serve report ../report/html")  # 查看报告