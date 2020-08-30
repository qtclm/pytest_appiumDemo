import os
import time
import pytest
import allure


# pytest第三方插件
    # 1，调整测试用例的执行顺序
        # 场景:未考虑按自然顺序执行时，或想变更执行顺序，比如增加 数据的用例要先执行，再执行删除的用例。测试用例默认是按名 称顺序执行的。
        # • 解决:
        # • 安装:pip install pytest-ordering
        # • 在测试方法上加下面装饰器
        # •@pytest.mark.last　　　　—最后一个执行
        # • @pytest.mark.run(order=1)—第几个执行
    # 2.解决用例依赖问题：pytest-dependency
        # 使用教程：
        #     https: // pytest - dependency.readthedocs.io / en / stable / usage.html  # basic-usage
@allure.feature("饿了么开通模块")
class Test_eleOpen:

    @pytest.fixture(scope='function')
    def eleOpenpage(self,platformServer):
        page = platformServer.jump_to_eleOpenPage()
        yield page
        page.control_back(num=2)


    @pytest.mark.run(order=1)
    # @pytest.mark.skip(reason='测试以通过，暂不运行')
    @allure.story('饿了么开通')
    @pytest.mark.dependency(name='eleOpen')
    def test_eleOpen(self,eleOpenpage):
        # page.log.info("测试饿了么开通页面")
        assert_list=['饿了么外卖开通','下一步','极速开店','当前绑定的客如云门店：','协助运维/销售信息（选填）']
        eleOpenpage.batch_assert(assert_obj=assert_list)

    @pytest.mark.run(order=2)
    @allure.story("极速开店页面")
    @pytest.mark.dependency(name='speedOpenShop',depends=['eleOpen'])
    def test_speedOpenShop(self,eleOpenpage):
        page=eleOpenpage.jump_to_speedOpenShopPage()
        assert_list=['饿了么开店','极速开店','获取验证码','协助运维/销售信息（选填）']
        page.batch_assert(assert_obj=assert_list)
        page.control_back(num=1)


    @pytest.mark.run(order=3)
    @allure.story("饿了么授权页面")
    @pytest.mark.dependency(name='eleAuth',depends=['eleOpen'])
    def test_eleAuth(self,eleOpenpage):
        page=eleOpenpage.jump_to_eleAuthPage()
        assert_list=['饿了么授权验证','手机验证码登录','登录','授权']
        page.batch_assert(assert_obj=assert_list)


if __name__=='__main__':
    os.system("pytest test_eleOpenPage.py")
    # os.system("pytest test_demo_shishike.py --maxfail=2")
    # pytest.main(['-s', '-q', '--alluredir', '../report/xml'])
    # os.system("allure generate --clean ../report/xml/ -o ../report/html")#生成allure报告
    # os.system("pytest --alluredir ../report/html/")#生成allure报告
    # os.system("allure serve report ../report/html")  # 查看报告