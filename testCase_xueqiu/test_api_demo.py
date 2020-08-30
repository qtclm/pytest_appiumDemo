from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.extensions.android.gsm import GsmCallActions
from appium.webdriver.common.mobileby import MobileBy
from tool.OperationDatas import OperationYaml

class TestDemo(object):
    def setup(self):
        yaml = OperationYaml(file_path='devices_caps_ApiDemos.yaml')
        caps = yaml.readforKey_onetier('caps')
        self.driver= webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(10)  # 添加隐式等待


    def test_toast(self):
        self.driver.find_element_by_accessibility_id("Views").click()

        # self.driver.swipe()
        # self.driver.find_element_by_accessibility_id("Popup Menu").click()

        self.driver.find_element_by_android_uiautomator('new UiScrollable(\
            new UiSelector().scrollable(true).instance(0)).\
            scrollIntoView(new UiSelector().text("Popup Menu").instance(0));').click()
        self.driver.find_element_by_accessibility_id("Make a Popup!").click()
        assert len(self.driver.find_elements_by_xpath("//*[@text='Edit']"))==1
        self.driver.find_element_by_xpath("//*[@text='Search']").click()
        # print(self.driver.find_element_by_xpath("//*[@class='android.widget.Toast']").text)
        assert "Clicked popup menu item Search" in self.driver.find_element_by_xpath("//*[@class='android.widget.Toast']").text

    # def test_gsm_call(self):
    #     self.driver.send_sms("18883612485","今天收入10086,余额1008610086")#模拟发短信
    #     self.driver.make_gsm_call("18883612485",GsmCallActions.CALL)#模拟打电话

    # # 获取性能数据
    # def test_performance(self):
    #     print(self.driver.get_performance_data_types())
    #     for p in self.driver.get_performance_data_types():
    #         try:
    #             print(self.driver.get_performance_data("com.xueqiu.android", p, 5))
    #         except :
    #             pass

    def teardown(self):
        self.driver.quit()


if __name__=='__main__':
    import os
    os.system("cd F:\\appium_temp && pytest test_api_demo.py")
    # os.system("cd F:\\appium_temp && pytest %s"%(__file__))