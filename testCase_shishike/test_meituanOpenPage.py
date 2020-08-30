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

@allure.feature("美团开通模块")
class Test_meituanOpen():
    toast_text = '开发中'

    @pytest.fixture(scope='function')
    def meituanOpenpage(self, platformServer):
        page = platformServer.jump_to_meituanOpenPage()
        yield page
        page.control_back(num=2)

    @pytest.mark.run(order=1)
    # @pytest.mark.skip(reason='测试以通过，暂不运行')
    @pytest.mark.dependency(name='meituanOpen')
    @allure.story('美团开通')
    def test_meituanOpenPage(self,meituanOpenpage):
        assert_list=['美团外卖','已开通','商品映射','商品管理','库存管理']
        meituanOpenpage.batch_assert(assert_obj=assert_list)

    @pytest.mark.run(order=2)
    @pytest.mark.dependency(name='goodsMapping',depends=['meituanOpen'])
    @allure.story('商品映射')
    def test_goodsMapping(self,meituanOpenpage):
        page=meituanOpenpage.jump_to_goodsMappingPage()
        assert_list=['全部','美团外卖','客如云','自动映射','删除映射']
        page.batch_assert(assert_obj=assert_list)
        page.control_back(num=1)

    @pytest.mark.run(order=3)
    @pytest.mark.dependency(name='goodsManagePage', depends=['meituanOpen'])
    @allure.story('商品管理')
    def test_goodsManagePage(self,meituanOpenpage):
        page=meituanOpenpage.jump_to_goodsManagePage()
        assert_list=[page.get_toast(text=self.toast_text)]
        page.batch_assert(assert_obj=assert_list,first_timeout=0.5)

    @pytest.mark.run(order=4)
    @pytest.mark.dependency(name='stocksManagePage', depends=['meituanOpen'])
    @allure.story('库存管理')
    def test_stockManagePage(self,meituanOpenpage):
        page=meituanOpenpage.jump_to_stockManagePage()
        assert_list=[page.get_toast(text=self.toast_text)]
        page.batch_assert(assert_obj=assert_list,first_timeout=0.5)



if __name__=='__main__':
    os.system("pytest test_meituanOpenPage.py")
    # os.system("cd F:\\appium_temp && pytest test_demo_shishike.py")
    # os.system("pytest test_demo_shishike.py --maxfail=2")
    # pytest.main(['-s', '-q', '--alluredir', '../report/xml'])
    # os.system("allure generate --clean ../report/xml/ -o ../report/html")#生成allure报告
    # os.system("pytest --alluredir ../report/html/")#生成allure报告
    # os.system("allure serve report ../report/html")#查看报告
