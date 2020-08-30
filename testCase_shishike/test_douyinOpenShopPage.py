import os
import time
import pytest
import allure

@allure.feature("抖音开店模块")
class Test_douyinOpenShop():

    @pytest.fixture(scope='function')
    def douyinOpenShopPage(self, platformServer):
        page = platformServer.jump_to_douyinOpenShopPage()
        yield page
        page.control_back(num=2)

    @pytest.mark.run(order=1)
    @allure.story('抖音开店页面')
    # @pytest.mark.skip(reason='测试以通过，暂不运行')
    @pytest.mark.dependency(name='douyinOpenShop')
    def test_douyinOpenShopPage(self, douyinOpenShopPage):
        assert_list = ['抖音开店', '用户协议和隐私条款', '获取验证码']
        douyinOpenShopPage.batch_assert(assert_obj=assert_list)

    @pytest.mark.run(order=2)
    @allure.story('抖音开店页面-输入手机号、验证码，点击下一步')
    @pytest.mark.dependency(name='douyin', depends=['douyinOpenShop'])
    def test_douyinPage(self,douyinOpenShopPage):
        page=douyinOpenShopPage.jump_to_douyinPage()
        toast_text='手机号和申请短信验证的手机号不符'
        assert_list = [page.get_toast(text=toast_text)]
        page.batch_assert(assert_obj=assert_list,first_timeout=0.5)

if __name__=='__main__':
    os.system("pytest test_douyinOpenShopPage.py")
    # os.system("cd F:\\appium_temp && pytest test_demo_shishike.py")
    # os.system("pytest test_demo_shishike.py --maxfail=2")
    # pytest.main(['-s', '-q', '--alluredir', '../report/xml'])
    # os.system("allure generate --clean ../report/xml/ -o ../report/html")#生成allure报告
    # os.system("pytest --alluredir ../report/html/")#生成allure报告
    # os.system("allure serve report ../report/html")#查看报告