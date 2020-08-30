from Common.BasePage import basePage
from xueqiuPages.main_page import MainPage


class LoginPage(basePage):

    _telLogin_locator = (basePage.by.ID, "com.xueqiu.android:id/tv_login_by_phone_or_others")
    _mailTelPasswordLogin_locator = (basePage.by.ID, "com.xueqiu.android:id/tv_login_with_account")
    _userInput_locator = (basePage.by.ID, "com.xueqiu.android:id/login_account")
    _passwordInput_locator = (basePage.by.ID, "com.xueqiu.android:id/login_password")
    _loginButton_locator = (basePage.by.ID, "com.xueqiu.android:id/button_next")

    # 跳转至搜索页面
    def tel_password_login(self):
        self.log.info("点击手机及其他登录按钮")
        self.click_button(self._telLogin_locator)
        self.log.info("点击邮箱手机号密码登录")
        self.click_button(self._mailTelPasswordLogin_locator)
        self.log.info("输入手机号")
        self.send_keys(self._userInput_locator,'18883612485')
        self.log.info("输入密码")
        self.send_keys(self._passwordInput_locator,'xphtcl55')
        self.log.info("点击登录按钮")
        self.click_button(self._loginButton_locator)
        return MainPage(self.driver)


if __name__=="__main__":
    from Common.app import App
    app=App.startApp()
    LoginPage(app).tel_login()