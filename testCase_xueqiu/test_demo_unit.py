import unittest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction


class TestDemo(unittest.TestCase):
    def setUp(self):
        caps = {}
        caps["platformName"] = "android"
        caps["appPackage"] = "com.xueqiu.android"
        caps["deviceName"] = "qtclm"
        caps["appActivity"] = ".view.WelcomeActivityAlias"
        caps['unicodeKeyboard']=True#resetKeyBoard是否需要输⼊⾮英⽂之外的语⾔并在测试完成后重置输⼊法
        caps['autoGrantPermissions']=True#⾃动赋予App权限
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(10)  # 添加隐式等待

    def test_demo(self):
        el1 = self.driver.find_element_by_id("com.xueqiu.android:id/tv_agree")
        el1.click()
        # TouchAction(self.driver).long_press().move_to().release().perform()  # 长按、拖动、释放、执行
        # self.driver.swipe()  # 滑动api，对TouchAction进行了一些简单的封装
        el2 = self.driver.find_element_by_id("com.xueqiu.android:id/home_search")
        el2.click()
        el3 = self.driver.find_element_by_id("com.xueqiu.android:id/search_input_text")
        el3.send_keys("alibaba")
        el3.click()
        el4 = self.driver.find_element_by_xpath(
            "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.LinearLayout/android.widget.TextView[1]")
        el4.click()

    def test_capabilities(self):
        el1 = self.driver.find_element_by_id("com.xueqiu.android:id/tv_agree")
        el1.click()
        # TouchAction(self.driver).long_press().move_to().release().perform()  # 长按、拖动、释放、执行
        # self.driver.swipe()  # 滑动api，对TouchAction进行了一些简单的封装
        el2 = self.driver.find_element_by_id("com.xueqiu.android:id/home_search")
        el2.click()
        el3 = self.driver.find_element_by_id("com.xueqiu.android:id/search_input_text")
        el3.send_keys("阿里巴巴")
        el3.click()


    def tearDown(self):
        self.driver.quit()


if __name__=='__main__':
    unittest.main()