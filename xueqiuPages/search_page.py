import time
from Common.BasePage import basePage

class SearchPage(basePage):

    _input_locator=(basePage.by.ID, "com.xueqiu.android:id/search_input_text")
    _name_locator=(basePage.by.ID, "name")
    _current_price=(basePage.by.ID,"current_price")

    # 执行搜索
    def search(self, keyword):
        self.log.info(f"输入文字:{keyword}")
        self.send_keys(self._input_locator,keyword)
        self.log.info("隐式等待5秒")
        self.wait_element(time=5)
        self.log.info("点击搜索出来的内容")
        self.click_button(self._name_locator)
        return self

    # 获取股价
    def get_current_price(self):
        self.log.info("获取股价")
        return float(self.find_element(self._current_price).text)

