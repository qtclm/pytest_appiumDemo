import time
from Common.BasePage import basePage
from shishikePages.meituanOpenPage import meituanOpenPage
from shishikePages.eleOpenPage import eleOpenPage
from shishikePages.eleOpenShopPage import eleOpenShopPage
from shishikePages.douyinOpenShopPage import douyinOpenPage
from shishikePages.kuaishouOpenPage import kuaishouOpenPage
from shishikePages.meituanGroupBuyingPage import meituanGroupBuyingPage
from shishikePages.evaluateManagePage import evaluateManagePage
from shishikePages.koubeiConfigPage import koubeiConfigPage
from tool.Mongo_connect import Mongo_gldexp

class PlatformServerPage(basePage):
    gldexp_mongo = Mongo_gldexp()
    gldexp_mongo.delete_one_collection(collection_name='partnerShopInfo',
                                            search_col={"source": -92, "shopId": 810108953})#删除快手开店信息

    _meituanOpen_locator = (
    basePage.by.XPATH, basePage.get_xpath_loc(class_loc=basePage._class_locator, text_loc='美团开通'))  # 美团开通图标位置
    _eleOpen_locator = (
    basePage.by.XPATH, basePage.get_xpath_loc(class_loc=basePage._class_locator, text_loc='饿了么开通'))  # 饿了么开通图标位置
    _eleOpenShop_locator = (
    basePage.by.XPATH, basePage.get_xpath_loc(class_loc=basePage._class_locator, text_loc='饿了么开店'))  # 饿了么开店图标位置
    _douyinOpenShop_locator = (
    basePage.by.XPATH, basePage.get_xpath_loc(class_loc=basePage._class_locator, text_loc='抖音开店'))  # 抖音开店图标位置
    _kuaishouOpenShop_locator = (
    basePage.by.XPATH, basePage.get_xpath_loc(class_loc=basePage._class_locator, text_loc='快手开店'))  # 快手开店图标位置
    _meituanGroupBuying_locator = (
    basePage.by.XPATH, basePage.get_xpath_loc(class_loc=basePage._class_locator, text_loc='美团团购'))  # 美团团购图标位置
    _evaluateManage_locator = (
    basePage.by.XPATH, basePage.get_xpath_loc(class_loc=basePage._class_locator, text_loc='评价管理'))  # 评价管理图标位置
    _koubeiConfig_locator = (
    basePage.by.XPATH, basePage.get_xpath_loc(class_loc=basePage._class_locator, text_loc='口碑设置'))  # 口碑设置图标位置
    time.sleep(5)

    # 跳转至饿了么开通页面
    def jump_to_eleOpenPage(self):
        self.click_button(self._eleOpen_locator)
        return eleOpenPage(self.driver)

    # 跳转至美团开通页面
    def jump_to_meituanOpenPage(self):
        self.click_button(self._meituanOpen_locator)
        return meituanOpenPage(self.driver)


    # 跳转至饿了么开店开通页面
    def jump_to_eleOpenShopPage(self):
        self.click_button(self._eleOpenShop_locator)
        return eleOpenShopPage(self.driver)

    # 跳转至抖音开店页面
    def jump_to_douyinOpenShopPage(self):
        self.click_button(self._douyinOpenShop_locator)
        return douyinOpenPage(self.driver)

    # 跳转至快手开店页面
    def jump_to_kuaishouOpenShopPage(self):
        self.click_button(self._kuaishouOpenShop_locator)
        return kuaishouOpenPage(self.driver)

    # 跳转至美团团购页面
    def jump_to_meituanGroupBuyingPage(self):
        self.click_button(self._meituanGroupBuying_locator)
        return meituanGroupBuyingPage(self.driver)

    # 跳转至评价管理页面
    def jump_to_evaluateManagePage(self):
        self.click_button(self._evaluateManage_locator)
        return evaluateManagePage(self.driver)

    # 跳转至口碑配置页面
    def jump_to_koubeiConfigPage(self):
        self.click_button(self._koubeiConfig_locator)
        return koubeiConfigPage(self.driver)
