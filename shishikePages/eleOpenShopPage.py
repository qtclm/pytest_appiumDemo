from Common.BasePage import basePage

class eleOpenShopPage(basePage):
    _speedOpenShop_locator=(basePage.by.XPATH,basePage.get_xpath_loc(
        class_loc=basePage._classButton_locator,text_loc='极速开店'))


    def jump_to_speedOpenShopPage(self):
        # 切换元素定位引擎为web，chromeDriver
        self.swith_locEngine(engine_type='web')
        label = 'input'
        property_key='placeholder'
        property_list=['请输入验证码','请填写姓名','请填写工号']
        for i in property_list:
            self.webview_xpath(label=label,property_key=property_key,property_value=i).send_keys('test_1')
        # 切换定位引擎为appium
        self.swith_locEngine(engine_type='app')
        self.click_button(loc=self._speedOpenShop_locator)
        return self



if __name__=="__main__":
    from Common.app import App
    el=eleOpenShopPage(App.startApp())