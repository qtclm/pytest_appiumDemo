# This sample code uses the Appium python client
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from appium import webdriver
from time import sleep

from appium.webdriver.common.touch_action import TouchAction

caps = {}
caps["platformName"] = "android"
caps["appPackage"] = "com.xueqiu.android"
caps["deviceName"] = "qtclm"
caps["appActivity"] = ".view.WelcomeActivityAlias"

driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
driver.implicitly_wait(10) #添加隐式等待

el1 = driver.find_element_by_id("com.xueqiu.android:id/tv_agree")
el1.click()

TouchAction(driver).long_press().move_to().release().perform()#长按、拖动、释放、执行
driver.swipe()#滑动api，对TouchAction进行了一些简单的封装
el2 = driver.find_element_by_id("com.xueqiu.android:id/home_search")
el2.click()
el3 = driver.find_element_by_id("com.xueqiu.android:id/search_input_text")
el3.send_keys("alibaba")
el3.click()
el4 = driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.RelativeLayout[1]/android.widget.LinearLayout/android.widget.TextView[1]")
el4.click()

driver.quit()