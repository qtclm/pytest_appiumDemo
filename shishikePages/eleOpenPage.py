from shishikePages.meituanOpenPage import meituanOpenPage

class eleOpenPage(meituanOpenPage):
    _speedOpenShop_locator = (
        meituanOpenPage.by.XPATH, meituanOpenPage.get_xpath_loc(class_loc=meituanOpenPage._class_locator, text_loc='极速开店'))  # 极速开店图标位置
    _nextStep_locator = (
        meituanOpenPage.by.XPATH, meituanOpenPage.get_xpath_loc(class_loc=meituanOpenPage._classButton_locator, text_loc='下一步'))  # 下一步图标位置

    def jump_to_speedOpenShopPage(self):
        self.click_button(self._speedOpenShop_locator)
        return self

    def jump_to_eleAuthPage(self):
        self.click_button(self._nextStep_locator)
        return self

