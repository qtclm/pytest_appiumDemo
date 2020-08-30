from Common.BasePage import basePage

class meituanGroupBuyingPage(basePage):
    _bindingSuccess_locator = (
        basePage.by.XPATH, basePage.get_xpath_loc(class_loc=basePage._class_locator, text_loc='已绑定成功'))  # 美团开通图标位置

    def display_page(self):
        self.wait_displayed(self._bindingSuccess_locator)
        return self