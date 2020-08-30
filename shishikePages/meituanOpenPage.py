from Common.BasePage import basePage

class meituanOpenPage(basePage):

    _goodsMapping_locator = (
        basePage.by.XPATH, basePage.get_xpath_loc(class_loc=basePage._class_locator, text_loc='商品映射'))  # 商品映射图标位置
    _goodsManage_locator = (
        basePage.by.XPATH, basePage.get_xpath_loc(class_loc=basePage._class_locator, text_loc='商品管理'))  # 商品管理图标位置
    _stockManage_locator = (
        basePage.by.XPATH, basePage.get_xpath_loc(class_loc=basePage._class_locator, text_loc='库存管理'))  # 库存管理图标位置

    def jump_to_goodsMappingPage(self):
        self.click_button(self._goodsMapping_locator)
        return self

    def jump_to_goodsManagePage(self):
        self.click_button(self._goodsManage_locator)
        return self

    def jump_to_stockManagePage(self):
        self.click_button(self._stockManage_locator)
        return self