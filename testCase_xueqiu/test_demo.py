import os
import pytest
import yaml
from time import sleep
from hamcrest import *
from Common.app import App
from Common.DataDriverCase import TestCase

class TestDemo(object):
    search_data=yaml.safe_load(open("./datas/search.yaml","r"))
    # print(search_data)
    def setup(self):
        self.driver = App.startApp()
        self.log=App.log

    # def test_a(self)a
    #     # 获取权限，弹窗，并点击允许
    #     self.driver.find_element_by_id("com.xueqiu.android:id/tv_open").click():
    #     self.driver.find_element_by_id("com.android.permissioncontroller:id/permission_allow_button").click()
    #     self.driver.find_element_by_id("com.android.permissioncontroller:id/permission_allow_button").click()

    # def test_xpath(self):
    #     self.driver.find_element_by_xpath("//*[@text='林园最新观点：上证指数超过4300点 才会进入真正的牛市' and contains(@resource-id,'topic_text')]").click()

    # @pytest.mark.parametrize("keyword,excepted_price",search_data)
    # def test_search_from_yaml(self,keyword,excepted_price):
    #     self.driver.search(keyword=keyword)
    #     price=self.driver.get_current_price()
    #     self.log.info(f"price:{price}")
    #     # print(price)
    #     assert float(price)>excepted_price
    #     # assert_that(price.get_attribute("package"),equal_to("com.xueqiu.android"))


    def test_search_from_yaml(self):
        self.log.info("执行测试")
        self.driver.to_search()
        TestCase().run(self.driver)

    # def test_market_from_yaml(self):
    #     self.log.info("执行测试")
    #     TestCase().run(self.driver)
    #
    # def test_deal_from_yaml(self):
    #     self.log.info("执行测试")
    #     TestCase().run(self.driver)
    #
    # def test_my_from_yaml(self):
    #     self.log.info("执行测试")
    #     TestCase().run(self.driver)

    def teardown(self):
        App.quit()



if __name__=='__main__':
    os.system("cd F:\\appium_temp && pytest test_demo.py")
    # ts=TestDemo()
    # ts.test_search_from_yaml()