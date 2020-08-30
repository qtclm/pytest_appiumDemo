import os
import time
import pytest
import allure

@allure.feature("评价管理模块")
class Test_evaluateManage():

    @pytest.fixture(scope='function')
    def evaluateManagePage(self, platformServer):
        page = platformServer.jump_to_evaluateManagePage()
        yield page
        page.control_back(num=2)

    @pytest.mark.run(order=1)
    # @pytest.mark.skip(reason='测试以通过，暂不运行')
    @allure.story('评价列表')
    @pytest.mark.dependency(name='evaluateList')
    def test_evaluateManagePage(self, evaluateManagePage):
        page = evaluateManagePage.jump_to_evaluatePage()
        assert_list = ['是否回复 ', '评价类型 ', '昨天 ']
        page.batch_assert(assert_obj=assert_list)

if __name__=='__main__':
    os.system("pytest test_evaluateManagePage.py")