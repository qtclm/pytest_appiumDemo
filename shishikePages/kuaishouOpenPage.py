from Common.BasePage import basePage


class kuaishouOpenPage(basePage):
    _inputOpInfo_locator=(basePage.by.XPATH,basePage.get_xpath_loc(text_loc='输入运维信息',class_loc=basePage._class_locator))
    _kuaishouAuth_locator=(basePage.by.XPATH,basePage.get_xpath_loc(text_loc='同意授权',class_loc=basePage._class_locator))
    _iWantAuth_locator=(basePage.by.XPATH,basePage.get_xpath_loc(text_loc='我要认证',class_loc=basePage._class_locator))


    def jump_to_kuaishouOpenAuthPage(self):
        self.click_button(self._inputOpInfo_locator)
        self.swith_locEngine(engine_type='web')
        property_list = ['请请输入协助运维/销售姓名', '请输入协助运维/销售工号']
        label = 'input'
        property_key = 'placeholder'
        for i in property_list:
            self.webview_xpath(label=label, property_key=property_key, property_value=i).send_keys('test1')
        self.webview_xpath(label='a',property_key='class',property_value='am-modal-button').click()#点击保存
        self.webview_xpath(label=label,property_key='class',property_value='am-checkbox-input').click()#点击同意协议
        self.swith_locEngine(engine_type='app')
        self.click_button(self._kuaishouAuth_locator)
        return self

    def jump_to_iWantAuthPage(self):
        self.click_button(self._iWantAuth_locator)
        return self


if __name__=="__main__":
    gldexp=Mongo_gldexp()
    gldexp.delete_one_collection(collection_name='partnerShopInfo',
                                            search_col={"source": -92, "shopId": 810108953})
