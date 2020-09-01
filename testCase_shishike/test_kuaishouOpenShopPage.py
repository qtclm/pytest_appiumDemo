import os
import time
import pytest
import allure

@allure.feature("快手开店模块")
class Test_kuaishouOpenShop():

    @pytest.fixture(scope='function')
    def kuaishouShopPage(self, platformServer):
        page = platformServer.jump_to_kuaishouOpenShopPage()
        yield page
        page.control_back(num=2)

    @pytest.mark.run(order=1)
    @allure.story('快手开店页面')
    @pytest.mark.skip(reason='测试以通过，暂不运行')
    @pytest.mark.dependency(name='kuaishouOpenShop')
    def test_kuaishouOpenShopPage(self, kuaishouShopPage):
        assert_list = ['同意授权', '输入运维信息', '《商家授权协议》']
        kuaishouShopPage.batch_assert(assert_obj=assert_list)

    @pytest.mark.run(order=2)
    @pytest.mark.skip(reason='测试以通过，暂不运行')
    @allure.story('快手开店页面-输入运维信息-点击授权')
    @pytest.mark.dependency(name='kuaishouOpenAuth', depends=['kuaishouOpenShop'])
    def test_kuaishouOpenAuthPage(self, kuaishouShopPage):
        page = kuaishouShopPage.jump_to_kuaishouOpenAuthPage()
        assert_list = ['我要认证','POI信息已导入成功','赶快去畅想快手海量流量吧！','可继续进行商家号认证操作，','可继续进行商家号认证操作，']
        page.batch_assert(assert_obj=assert_list)

    @pytest.mark.run(order=3)
    @pytest.mark.skip(reason='测试以通过，暂不运行')
    @allure.story('快手开店页面-点击我要导入，跳转快手登录页面')
    @pytest.mark.dependency(name='iWantAuth', depends=['kuaishouOpenAuth'])
    def test_kuaishouiWantAuthPage(self, kuaishouShopPage):
        page = kuaishouShopPage.jump_to_iWantAuthPage()
        assert_list = ['快手第三方登录', '手机号登录', '下一步']
        page.batch_assert(assert_obj=assert_list)


if __name__=='__main__':
    os.system("pytest test_kuaishouOpenShopPage.py")
    # os.system("pytest test_demo_shishike.py --maxfail=2")
    # pytest.main(['-s', '-q', '--alluredir', '../report/xml'])
    # os.system("allure generate --clean ../report/xml/ -o ../report/html")#生成allure报告
    # os.system("pytest --alluredir ../report/html/")#生成allure报告
    # os.system("allure serve report ../report/html")  # 查看报告