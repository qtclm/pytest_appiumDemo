from Common.BasePage import basePage
from  shishikePages.mainPage import MainPage


class LoginPage(basePage):

    _loadBgImg_locator = (basePage.by.ID, "com.shishike.mobile:id/load_bg_img")  # 加载背景图，用于判断app是否重启完成
    _logo_locator = (basePage.by.ID, "com.shishike.mobile:id/iv_logo")#shishike logo
    _env_SelectName="com.shishike.mobile:id/tv_common_name"#环境选择输入框
    _gldEnv_locator = (basePage.by.XPATH, basePage.get_xpath_loc(id_loc=_env_SelectName,text_loc='GldEnv'))  # gld环境
    _devEnv_locator = (basePage.by.XPATH, basePage.get_xpath_loc(id_loc=_env_SelectName,text_loc='DevEnv'))  # DevEnv环境
    _citestEnv_locator = (basePage.by.XPATH, basePage.get_xpath_loc(id_loc=_env_SelectName,text_loc='CITestEnv'))  # CITestEnv环境
    _releaseEnv_locator = (basePage.by.XPATH, basePage.get_xpath_loc(id_loc=_env_SelectName,text_loc='ReleaseEnv'))  # ReleaseEnv环境
    _singaporeEnv_locator = (basePage.by.XPATH, basePage.get_xpath_loc(id_loc=_env_SelectName,text_loc='SingaporeEnv'))  # SingaporeEnv环境
    _promptlyExp_locator = (basePage.by.ID, "com.shishike.mobile:id/enter_btn")#立即体验按钮
    _loginUserName_locator = (basePage.by.ID, "com.shishike.mobile:id/id_ed_login_username")#登录手机号
    _loginPassword_locator = (basePage.by.ID, "com.shishike.mobile:id/id_ed_login_password")#登录密码
    _loginButton_locator = (basePage.by.ID, "com.shishike.mobile:id/loginBut")#登录按钮
    _shopInfo_selectName="com.shishike.mobile:id/account_item_org_tv_name"#门店选择



    # 跳转至登录页面
    def jump_to_login(self):
        self.swipe_Rigth()
        self.swipe_Rigth()
        self.click_button(self._promptlyExp_locator)

    # 切换环境
    def env_cut(self,env=None):
        self.jump_to_login()
        for i in range(5):
            self.click_button(self._logo_locator)
        if env=='dev':
            self.log.info('切换环境至dev')
            self.click_button(self._devEnv_locator)
        elif env == 'citest':
            self.log.info('切换环境至citest')
            self.click_button(self._citestEnv_locator)
        elif env in('release','prod'):
            self.log.info('切换环境至release')
            self.click_button(self._releaseEnv_locator)
        elif env == 'singapore':
            self.log.info('切换环境至singapore')
            self.click_button(self._singaporeEnv_locator)
        else:
            self.log.info('切换环境至gld')
            self.click_button(self._gldEnv_locator)
        self.log.info('等待app重启完毕，延时15秒')
        self.wait_displayed(loc=self._loadBgImg_locator,time_out=15)


    # 登录
    def login(self,username,password):
        self.log.info("跳转至登录页面")
        self.jump_to_login()
        self.send_keys(self._loginUserName_locator,username)
        self.send_keys(self._loginPassword_locator,password)
        self.click_button(self._loginButton_locator)
        return self


    # 选择店铺
    def select_shop(self,shopName):
        _shopName_locator=(basePage.by.XPATH,self.get_xpath_loc(id_loc=self._shopInfo_selectName,text_loc=shopName))
        self.autoSwipe_demo(loc=shopName,swipe_mode='up')
        # self.autoSwipeToObjElement(object_loc=shopName)
        self.click_button(_shopName_locator)
        return MainPage(self.driver)




if __name__=="__main__":
    from Common.app import App
    app=App.startApp()
    LoginPage(app).env_cut()