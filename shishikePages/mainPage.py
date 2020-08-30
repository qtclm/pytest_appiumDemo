import time

from Common.BasePage import basePage
from shishikePages.platformServerPage import PlatformServerPage

class MainPage(basePage):

    _main_icon_id='com.shishike.mobile:id/main_menu_tv' #首页icon
    _platformServer_locator = (basePage.by.XPATH, basePage.get_xpath_loc(id_loc=_main_icon_id,text_loc='平台服务'))  #平台服务图标位置
    _littleOn_locator=(basePage.by.ID,'com.shishike.mobile:id/tv_home_samll_on_exit') #小on图标关闭,避免直接进入饿了么开通页面

    #关闭小on
    def close_littleon(self):
        self.loc_displayed(loc=self._littleOn_locator, time_out=3,time_all=6)
        self.click_button(self._littleOn_locator)
        return self

    # 跳转到平台服务页面
    def jump_to_platformServerPage(self):
        self.loc_displayed(loc=self._platformServer_locator, time_out=0.1)
        self.click_button(self._platformServer_locator)
        return PlatformServerPage(self.driver)