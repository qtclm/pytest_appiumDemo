import os
import time
import pytest
import allure

@allure.feature("美团团购模块")
class Test_meituanGroupBuying():

    @pytest.fixture(scope='function')
    def meituanGroupBuyingPage(self, platformServer):
        page = platformServer.jump_to_meituanGroupBuyingPage()
        yield page
        page.control_back(num=2)

    @pytest.mark.run(order=1)
    @allure.story('美团团购页面')
    # @pytest.mark.skip(reason='测试以通过，暂不运行')
    @pytest.mark.dependency(name='meituanGroupBuying')
    def test_meituanGroupBuyingPage(self, meituanGroupBuyingPage):
        assert_list = ['美团团购', '已绑定成功']
        meituanGroupBuyingPage.batch_assert(assert_obj=assert_list)

if __name__=='__main__':
    os.system("pytest test_meituanGroupBuyingPage.py")