from Common.BasePage import basePage

class douyinOpenPage(basePage):
    _nextStep_locator = (basePage.by.XPATH, basePage.get_xpath_loc(
        class_loc=basePage._classButton_locator, text_loc='下一步'))

    def jump_to_douyinPage(self):
        self.swith_locEngine(engine_type='web')
        property_list=['请输入手机号码','请输入验证码']
        value_list=['18883612485','123456']
        label = 'input'
        property_key='placeholder'
        for i,value in zip(property_list,value_list):
            self.webview_xpath(label=label, property_key=property_key, property_value=i).send_keys(value)
        self.webview_xpath(label=label, property_key='class', property_value='am-checkbox-input').click()
        self.swith_locEngine(engine_type='app')
        self.click_button(loc=self._nextStep_locator)
        return self
