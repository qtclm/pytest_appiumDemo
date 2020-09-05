import os
import time
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from Common.importCommon import log


class basePage(log):
    # '''黑名单：业务之外的弹窗，但又会影响元素定位的一些元素，特殊处理
    #   1.升级弹窗
    #   2.广告弹窗
    #   3.用户隐私协议弹窗
    #   具体看app具体的处理细节'''
    by=MobileBy
    _back_locator=(by.ID, 'com.shishike.mobile:id/titlebar_iv_left_standard')  # 点击返回按钮
    _class_locator = 'android.view.View' #公用普通class组件定位字段
    _classButton_locator = 'android.widget.Button' #共用的class按钮定位字段
    _black_list = [
        # (MobileBy.ID, "com.xueqiu.android:id/image_cancel"),
        # (MobileBy.ID, "com.xueqiu.android:id/ib_close"),
        # (MobileBy.ID, "com.xueqiu.android:id/tv_agree"),
        _back_locator
    ]


    def __init__(self, driver: WebDriver):
        super().__init__()
        self.driver = driver

    # 隐式等待
    def wait_element(self,time=5):
        self.log.info(f"隐式等待{time}秒")
        self.driver.implicitly_wait(time)

    # 显示等待
    def wait_displayed(self,loc,time_out=3):
        try:
            WebDriverWait(self.driver, timeout=time_out).until(lambda driver: driver.find_element(*loc).is_displayed())
            return True
        except Exception as e:
            self.log.info('元素定位超时：{},重试中'.format(e))
            return False


    # 强行等待元素展示，超时时间为30s
    def loc_displayed(self,loc,time_out=5,time_all=30):
        while True:
            flag = self.wait_displayed(loc,time_out=time_out)
            time_all-=time_out
            if flag:
                break
            if time_all<=0:
                raise Exception('等待元素展示超时')

    def find_element(self, loc,time_out=5):
        # print("loc:{}".format(loc))
        try:
            self.log.info("查找元素{}".format(loc))
            count=1
            # 重试1次
            while count<2:
                flag = self.wait_displayed(loc=loc, time_out=time_out)
                if flag:
                    break
                else:
                    self.log.info('元素没有存在于当前页面中,当前重试次数为第{}次'.format(count))
                    count+=1
            return self.driver.find_element(*loc)
        except:
            error_info='页面中未能找到{}元素'.format(loc)
            self.log.error(error_info)
            self.getScreenShot()

    def find_elements(self, loc):
        '''封装一组元素定位方法'''
        try:
            self.log.info("查找元素{}".format(loc))
            if len(self.driver.find_elements(*loc)):
                return self.driver.find_elements(*loc)
        except Exception as e:
            error_info='页面中未能找到{}元素'.format(loc)
            self.log.error(error_info)
            self.getScreenShot()
            # print(error_info)
            # return False

    def clear_key(self, loc):
        """重写清空文本输入法"""
        try:
            self.find_element(loc).clear()
            self.log.info("清空文本{}".format(loc))
        except Exception as e:
            self.log.error("清空文本{}：失败，异常：{}".format(loc,e))


    def send_keys(self, loc, value):
        """重写在文本框中输入内容的方法"""
        self.clear_key(loc)  # 先调用
        try:
            self.find_element(loc).send_keys(value)
            self.log.info("输入文本{}".format(value))
        except Exception as e:
            self.log.error("输入文本{}：失败,异常：{}".format(loc,e))


    def click_button(self, loc):
        """重写点击按钮的方法"""
        try:
            self.find_element(loc).click()
            self.log.info("点击元素{}".format(loc))
        except Exception as e:
            self.log.error("点击元素{}失败,异常：{}".format(loc,e))

    def getScreenShot(self):
        """重写截图方法"""
        screenshot_path='../report/img/screenshot'
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        self.sh_file = os.path.join(screenshot_path, 'errorImg_%s.png' %(time.strftime("%Y%m%d%H%M%S")))
        self.log.info("屏幕截图为：{}".format(self.sh_file))
        try:
            self.driver.get_screenshot_as_file(self.sh_file)
        except Exception as e:
            self.log.error("截图失败,异常：{}".format(e))

    def get_windows_size(self):
        """获取屏幕大小"""
        self.log.info("获取屏幕大小")
        try:
            windows_size = self.driver.get_window_size()
            self.log.info('屏幕大小为{}'.format(windows_size))
            return windows_size
        except Exception as e:
            self.getScreenShot()
            self.log.error("获取屏幕大小失败,异常：{}".format(e))

    #滑动屏幕公共方法
    def swipe_common(self,w_start,h_start,w_end,h_end,swipe_time):
        '''w_start:宽度开始位置，w_end：宽度结束位置
        h_start:高度开始位置，h_end：高度结束位置'''
        window_size = self.get_windows_size()
        width = window_size.get("width")
        height = window_size.get("height")
        width_start=width * w_start
        height_start=height * h_start
        width_end=width * w_end
        height_end=height * h_end
        self.log.info('宽度起始值：{},高度起始值：{},宽度结束值：{},高度结束值：{}'.format(width_start,height_start,width_end,height_end))
        # time.sleep(1)
        self.driver.swipe(width_start,height_start,width_end,height_end, swipe_time)
        # time.sleep(1)

    def swipe_Up(self,loc_ratio=0.5,start=0.8,end=0.3,swipe_time=500):
        '''loc_ratio:屏幕位置比例，start:开始滑动的区域，end：结束滑动的区域，swipe_time：滑动持续时间'''
        '''上滑'''
        self.log.info("上滑")
        try:
            self.swipe_common(w_start=loc_ratio,h_start=start,w_end=loc_ratio,h_end=end,swipe_time=swipe_time)
        except Exception as e:
            self.getScreenShot()
            self.log.error("上滑失败,异常：{}".format(e))

    def swipe_Down(self,loc_ratio=0.5,start=0.3,end=0.8,swipe_time=500):
        '''下滑'''
        self.log.info("下滑")
        try:
            self.swipe_common(w_start=loc_ratio,h_start=start,w_end=loc_ratio,h_end=end,swipe_time=swipe_time)
        except Exception as e:
            self.getScreenShot()
            self.log.error("下滑失败,异常：{}".format(e))

    def swipe_Left(self,loc_ratio=0.5,start=0.3,end=0.8,swipe_time=500):
        '''左滑'''
        self.log.info("左滑")
        try:
            self.swipe_common(w_start=start, h_start=loc_ratio, w_end=end, h_end=loc_ratio, swipe_time=swipe_time)
            # self.driver.swipe(width / 4, height / 2, width * 3 / 4, height / 2, 500)
        except Exception as e:
            self.getScreenShot()
            self.log.error("左滑失败,异常：{}".format(e))

    def swipe_Rigth(self,loc_ratio=0.5,start=0.8,end=0.3,swipe_time=500):
        '''右滑'''
        self.log.info("右滑")
        try:
            self.swipe_common(w_start=start, h_start=loc_ratio, w_end=end, h_end=loc_ratio, swipe_time=swipe_time)
            # self.driver.swipe(width * 4 / 5, height / 2, width / 5, height / 2, 500)
        except Exception as e:
            self.getScreenShot()
            self.log.error("右滑失败,异常：{}".format(e))

    def long_press(self,x1,y1,te=1500):
        '''长按'''
        self.log.info("长按")
        try:
            TouchAction(self.driver).long_press(x=x1,y=y1).wait(ms=te).release().perform()
        except Exception as e:
            self.getScreenShot()
            self.log.error("长按失败,异常：{}".format(e))

    def short_press(self, x1, y1):
        '''短按'''
        self.log.info("短按")
        try:
            TouchAction(self.driver).press(x=x1, y=y1).release().perform()
        except Exception as e:
            self.getScreenShot()
            self.log.error("短按失败,异常：{}".format(e))

    def move(self, x1, y1,x2,y2,te):
        '''拖动'''
        self.log.info("拖动")
        try:
            TouchAction(self.driver).long_press(x=x1, y=y1).wait(ms=te).move_to(x=x2,y=y2).release().perform()
        except Exception as e:
            self.getScreenShot()
            self.log.error("短按失败,异常：{}".format(e))

    # 自动滑动页面至指定位置,appium源码实现
    def autoSwipeToObjElement(self,object_loc):
        self.log.info('自动滑动元素至页面指定位置:{}'.format(object_loc))
        self.driver.find_element_by_android_uiautomator('new UiScrollable(\
                    new UiSelector().scrollable(true).instance(0)).\
                    scrollIntoView(new UiSelector().text("{}").instance(0));'.format(object_loc)).click()

    # 判断元素是否在当前页面
    def elemeIsInPageSourse(self,loc,loc_type='text',timeout=3):
        if loc_type in ('id','resource-id'):
            loc_type='resource-id'
        elif loc_type in ('text'):
            loc_type='text'
        elif loc_type in ('class'):
            loc_type='class'
        elif loc_type in ('packege'):
            loc_type='package'
        elif loc_type in ('content-desc'):
            loc_type='content-desc'
        else:
            raise Exception("暂不支持的元素类型")
        # todo: 使用page source会更快的定位
        time.sleep(timeout)
        page_source=self.driver.page_source
        # self.log.info('page_source:{}'.format(page_source))
        if isinstance(loc,(tuple,list)):
            if '{}="{}"'.format(loc_type,loc[1]) in page_source:
                return True
            self.getScreenShot()
            self.log.info('当前页面结构：\n{}'.format(page_source) )
            return False
        elif loc and '{}="{}"'.format(loc_type,loc) in page_source:
            return True
        self.log.info('当前页面结构：\n{}'.format(page_source))
        return False
        # self.log.info(page_source)
        # print(page_source)

    # 根据传入参数判定对应的滑动方式
    def Swipe_demo(self,swipe_mode):
        if swipe_mode == 'up':
            self.swipe_Up()
        elif swipe_mode == 'down':
            self.swipe_Down()
        elif swipe_mode == 'left':
            self.swipe_Left()
        elif swipe_mode == 'right':
            self.swipe_Rigth()
        else:
            raise Exception("暂不支持的滑动方式")

    # 封装自动滑动逻辑，默认只有十次滑动机会
    def autoSwipe_demo(self,loc,swipe_mode,timeout=3,swipe_num=10):
        count=1
        while count<=swipe_num:
            flag=self.elemeIsInPageSourse(loc,timeout=timeout)
            # print(flag)
            if flag:
                self.log.info("元素存在于当前页面中，停止滑动")
                break
            else:
                self.Swipe_demo(swipe_mode=swipe_mode)
                self.log.info('元素没有存在于当前页面中，执行滑动，滑动方式为：{},当前滑动次数为第{}次'.format(swipe_mode,count))
                count+=1


    ##处理公共异常
    def main_exception(self):
        self.log.info("开始处理公共异常")
        for loc in self._black_list:
            self.wait_displayed(loc=loc,time_out=3)
            elements = self.driver.find_elements(*loc)
            if len(elements) >= 1:
                # todo: 不是所有的弹框处理都是要点击弹框，可根据业务需要自行封装
                self.wait_element(time=1)
                elements[0].click()

            else:
                self.wait_displayed(loc=loc,time_out=1)
                print("%s not found" % str(loc))
                continue

    # 获取xpath定位表达式
    @staticmethod
    def get_xpath_loc(id_loc=None,text_loc=None,class_loc=None):
        # id、class 与text组合定位
        if id_loc and text_loc and class_loc:
            return "//*[@resource-id='{}'][@class='{}'][@text='{}']".format(id_loc, class_loc, text_loc)
        # id 与text组合定位
        elif id_loc and text_loc:
            return "//*[@resource-id='{}'][@text='{}']".format(id_loc,text_loc)
        # class 与text组合定位
        elif class_loc and text_loc:
            return "//*[@class='{}'][@text='{}']".format(class_loc, text_loc)
        elif class_loc:
            return "//*[@class='{}']".format(class_loc)
        elif text_loc:
            return "//*[@text='{}']".format(text_loc)
        else:
            # 直接访问整个页面的结构
            return '//*'

    #批量断言
    def batch_assert(self,assert_obj:(dict,list,tuple),first_timeout=5):
        for index,i in enumerate(assert_obj):
            if index==0:
                timeout=first_timeout
            else:
                timeout=0.01
            assert self.elemeIsInPageSourse(loc=i,timeout=timeout)

    #控制返回次数
    def control_back(self,num:int=2):
        for i in range(num):
            self.click_button(self._back_locator)

    #获取toast提示
    def get_toast(self,text,text_type='text'):
        if text_type=='class':
            toast_text=self.find_element(loc=(self.by.XPATH,self.get_xpath_loc(class_loc=text))).text
        else:
            toast_text=self.find_element(loc=(self.by.XPATH,self.get_xpath_loc(text_loc=text))).text
        self.log.info('toast:{}'.format(toast_text))
        return toast_text

    # 针对h5页面编写单独的xpath定位方式
    def webview_xpath(self,label,property_value,property_key='placeholder'):
        '''lable:标签名称，property_key:属性名，property_value:属性值'''
        return self.find_element(loc=(self.by.XPATH,'//{}[@{}="{}"]'.format(label,property_key,property_value)))

    #切换元素定位引擎
    def swith_locEngine(self,engine_type='WEBVIEW_'):
        '''app采用原生appium提供的定位方式，webview采用chromeDirver定位（请注意版本匹配，
        、当前app采用chrome68，对应的chromeDriver版本为2.39）,具体明细请参考：https://blog.csdn.net/BinGISer/article/details/88559532'''
        contexts=self.driver.contexts
        self.log.info('contexts:{}'.format(contexts))
        if engine_type in ('web','webView','web-view','web_view','WEBVIEW_','h5'):
            self.driver.switch_to.context(contexts[-1])
            self.log.info('swith to  locEngine:{}'.format(contexts[-1]))
        else:
            self.log.info('swith to locEngine :{}'.format(contexts[0]))
            self.driver.switch_to.context(contexts[0])



if __name__=="__main__":
    from Common.app import App
    bs=basePage(App.startApp().getScreenShot())
    # bs.getScreenShot()
    # print(ele.get_windows_size())
    # print(hasattr(MobileBy,'-ios predicate string'))