from Common.BasePage import basePage
from xueqiuPages.search_page import SearchPage


class MainPage(basePage):
    # _search_locator = (basePage.by.ID, "com.xueqiu.android:id/tv_search")
    _search_locator = (basePage.by.ID, "com.xueqiu.android:id/home_search")
    _table_name="[@resource-id='com.xueqiu.android:id/tab_name']"
    _market_locator=(basePage.by.XPATH,"//*{}[@text='行情']".format(_table_name))
    _deal_locator=(basePage.by.XPATH,"//*{}[@text='交易']".format(_table_name))
    _my_locator=(basePage.by.XPATH,"//*{}[@text='我的']".format(_table_name))

    # 跳转至搜索页面
    def to_search(self):
        self.main_exception()
        self.log.info("点击搜索框")
        self.click_button(self._search_locator)
        self.wait_element(time=1)
        self.log.info('跳转至搜索页面')
        return SearchPage(self.driver)

    # 跳转至行情首页页面
    def to_marketPage(self):
        self.main_exception()
        self.click_button(self._market_locator)
        self.log.info('跳转至行情首页页面')

    # 跳转至交易首页页面
    def to_dealPage(self):
        self.main_exception()
        self.click_button(self._deal_locator)
        self.log.info('跳转至交易首页页面')

    # 跳转至我的页面
    def to_myPage(self):
        self.main_exception()
        self.click_button(self._my_locator)
        self.log.info('跳转至我的页面')


if __name__=='__main__':
    from Common.app import App
    app=App.startApp()
    # ma=MainPage(app)
    app.to_marketPage()
    app.to_dealPage()
    app.to_myPage()
    # ma.to_search().search(keyword="hello")

