from Common.importCommon import Tool
from Common.BasePage import basePage
from hamcrest import *

class TestCase(Tool):
    assert_value = ""  # 默认断言值
    def __init__(self,dataCase_path='../testcase/datas',file_path='testcase.yaml'):
        super().__init__(path=dataCase_path,file_path=file_path)
        self.steps=self.yaml.read_data()

    def run(self,driver:basePage):
        for step in self.steps:
            self.log.info("step:{}".format(step))
            # print(step)
            if isinstance(step, dict):
                # 元素操作定位部分
                self.ele_operation(dict_obj=step,driver=driver)
                # 设备操作部分
                self.devices_operation(dict_obj=step,driver=driver)
                #断言部分
                if self.assert_value :
                    # 匹配相等对象
                    self._assertCommon(dict_obj=step,assert_value=self.assert_value)

    # 元素操作定位部分
    def ele_operation(self, dict_obj, driver):
        element = None
        # 元素隐式等待
        if 'wait' in dict_obj.keys():
            driver.wait_element(time=dict_obj['wait'])

        '''元素定位部分'''
        if "id" in dict_obj.keys():
            element = driver.find_element(loc=(basePage.by.ID, dict_obj["id"]))
        elif "xpath" in dict_obj.keys():
            element = driver.find_element(loc=(basePage.by.XPATH, dict_obj["xpath"]))
        elif "accessibility_id" in dict_obj.keys():
            element = driver.find_element(loc=(basePage.by.ACCESSIBILITY_ID, dict_obj["accessibility_id"]))
        elif "android_uiautomator" in dict_obj.keys():
            element = driver.find_element(loc=(basePage.by.ANDROID_UIAUTOMATOR, dict_obj["android_uiautomator"]))
        else:
            self.log.info("暂不支持的定位方式")

        if element:
            '''元素操作部分'''
            if "input" in dict_obj.keys():
                element.send_keys(dict_obj["input"])
            # elif "click" in step.keys():
            #     element.click()
            # 获取text
            elif "get" in dict_obj.keys():
                self.assert_value = element.get_attribute(dict_obj["get"])
            else:
                element.click()

    # 设备操作
    def devices_operation(self,dict_obj,driver):
        # '''设备操作部分'''
        if 'screenShot' in dict_obj.keys():
            driver.getScreenShot()
        elif 'swipe_Up' in dict_obj.keys():
            driver.swipe_Up()
        elif 'swipe_Down' in dict_obj.keys():
            driver.swipe_Down()
        elif 'swipe_Left' in dict_obj.keys():
            driver.swipe_Left()
        elif 'swipe_Rigth' in dict_obj.keys():
            driver.swipe_Rigth()
        elif 'long_press' in dict_obj.keys():
            driver.long_press(x1=dict_obj['x1'], y1=dict_obj['y1'], te=dict_obj['te'])
        elif 'long_press' in dict_obj.keys():
            driver.long_press(x1=dict_obj['x1'], y1=dict_obj['y1'], te=dict_obj['te'])
        elif 'short_press' in dict_obj.keys():
            driver.short_press(x1=dict_obj['x1'], y1=dict_obj['y1'])
        elif 'move' in dict_obj.keys():
            driver.move(x1=dict_obj['x1'], y1=dict_obj['y1'], x2=dict_obj['x2'], y2=dict_obj['y2'], te=dict_obj['te'])
        else:
            self.log.info("暂不支持的操作方式")

  # 公用断言
    def _assertCommon(self,dict_obj,assert_value):
        if "assert_equal_to" in dict_obj.keys():
            assert_that(float(dict_obj['assert_equal_to']), equal_to(float(assert_value)))
        # 匹配大于
        elif "assert_greater_than" in dict_obj.keys():
            assert_that(float(dict_obj['assert_greater_than']), greater_than(float(assert_value)))
        # 匹配大于等于
        elif "assert_greater_than_or_equal_to" in dict_obj.keys():
            assert_that(float(dict_obj['assert_greater_than_or_equal_to']), greater_than_or_equal_to(float(assert_value)))
        # 匹配小于
        elif "assert_less_than" in dict_obj.keys():
            assert_that(float(dict_obj['assert_less_than']), less_than(float(assert_value)))
        # 匹配小于等于
        elif "assert_less_than_or_equal_to" in dict_obj.keys():
            assert_that(float(dict_obj['assert_less_than_or_equal_to']), less_than_or_equal_to(float(assert_value)))
        # 长度匹配 len()
        elif "assert_has_length" in dict_obj.keys():
            assert_that(dict_obj['assert_has_length'], has_length(assert_value))
        # 匹配字符串 str()
        elif "assert_has_string" in dict_obj.keys():
            assert_that(dict_obj['assert_has_string'], has_string(assert_value))
        # 匹配对象类型
        elif "assert_instance_of" in dict_obj.keys():
            assert_that(dict_obj['assert_instance_of'], instance_of(assert_value))
        # 匹配none
        elif "assert_none" in dict_obj.keys():
            assert_that(dict_obj['assert_none'], none(assert_value))
        # 匹配not none
        elif "assert_not_none" in dict_obj.keys():
            assert_that(dict_obj['assert_not_none'], not_none(assert_value))
        # 匹配字符串开头
        elif "assert_starts_with" in dict_obj.keys():
            assert_that(dict_obj['assert_starts_with'], starts_with(assert_value))
        # 匹配字符串结尾
        elif "assert_ends_with" in dict_obj.keys():
            assert_that(dict_obj['assert_ends_with'], ends_with(assert_value))
        # 匹配完整的字符串但忽略大小写
        elif "assert_equal_to_ignoring_case" in dict_obj.keys():
            assert_that(dict_obj['assert_equal_to_ignoring_case'], equal_to_ignoring_case(assert_value))
        # 匹配完整的字符串，但忽略多余的空格
        elif "assert_equal_to_ignoring_whitespace" in dict_obj.keys():
            assert_that(dict_obj['assert_equal_to_ignoring_whitespace'], equal_to_ignoring_whitespace(assert_value))
        # 使用正则表达式匹配字符串
        elif "assert_matches_regexp" in dict_obj.keys():
            assert_that(dict_obj['assert_matches_regexp'], matches_regexp(assert_value))
        # 完全匹配整个序列
        elif "assert_contains" in dict_obj.keys():
            assert_that(dict_obj['assert_contains'], contains(assert_value))
        # 以任何顺序匹配整个序列
        elif "assert_contains_inanyorder" in dict_obj.keys():
            assert_that(dict_obj['assert_contains_inanyorder'], matches_regexp(assert_value))
        else:
            assert False


if __name__=='__main__':
    TestCase()