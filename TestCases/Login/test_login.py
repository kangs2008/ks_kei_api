import pytest
import allure
import sys
import os
import unittest
from Datas.global_datas import invalid_data1, invalid_data2, pass_data
from Common.handle_logger import logger
from Common.utils import assertFalseMethod, assertTrueMethod, mTime
from Pages.LoginPage.login_page import LoginPage

@allure.feature("login 异常测试用例，feature")
@pytest.mark.usefixtures('start_session')
@pytest.mark.usefixtures('refresh_page')
class TestLogin:

    # 异常测试用例
    @allure.story("测试login 方法，story")
    @pytest.mark.parametrize('data', invalid_data1)
    # @allure.dynamic.title("aaaaa")
    def test_login(self, data, start_session):
        """描述！！！！"""
        logger.info(" 执行 {0} 测试套件Suite ".format(self.__class__.__name__))
        logger.info(" 执行 {0} 测试用例Case ".format(sys._getframe().f_code.co_name))

        LoginPage(start_session).login(data['user'], data['pwd'])
        LoginPage(start_session).login(data['user'], data['pwd'])
        logger.info(" 结束执行 {0} 测试用例， 测试结果 --- PASS ".format(sys._getframe().f_code.co_name))

    # 异常测试用例
    @allure.story("login 异常1，story")
    @pytest.mark.parametrize('data', invalid_data1)
    # @allure.dynamic.description('动态描述？')
    def test_login_user_error(self, data, start_session):
        allure.dynamic.description('动态描述？')
        logger.info(" 执行 {0} 测试套件Suite ".format(self.__class__.__name__))
        logger.info(" 执行 {0} 测试用例Case ".format(sys._getframe().f_code.co_name))

        LoginPage(start_session).input_username(data['user'])
        LoginPage(start_session).input_pwd(data['pwd'])
        LoginPage(start_session).login_btn()
        # msg = LoginPage(start_session).get_login_errMsg()
        msg = LoginPage(start_session).get_user_errMsg()
        logger.info("期望值：{0}".format(data['expect']))
        logger.info("实际值：{0}".format(msg))
        try:
            assertTrueMethod(msg, data['expect'])
            logger.info(" 结束执行 {0} 测试用例， 测试结果 --- PASS ".format(sys._getframe().f_code.co_name))
            LoginPage(start_session).save_screenshot("{0}-正常截图".format(data['user']))
        except:
            logger.error(" 结束执行 {0} 测试用例， 测试结果 --- False ".format(sys._getframe().f_code.co_name))
            LoginPage(start_session).save_screenshot("{0}-异常截图".format(data['user']))
            raise

    # 异常测试用例
    @allure.story("login 异常2，story")
    @pytest.mark.parametrize('data', invalid_data2)
    def test_login_pwd_error(self, data, start_session):
        allure.dynamic.title("aaaaa")
        logger.info(" 执行 {0} 测试套件Suite ".format(self.__class__.__name__))
        logger.info(" 执行 {0} 测试用例Case ".format(sys._getframe().f_code.co_name))

        try:
            LoginPage(start_session).input_username(data['user'])
            LoginPage(start_session).input_pwd(data['pwd'])
            LoginPage(start_session).login_btn()

            msg = LoginPage(start_session).get_pwd_errMsg()
            logger.info("期望值：{0}".format(data['expect']))
            logger.info("实际值：{0}".format(msg))
            assertTrueMethod(msg, data['expect'])
            msg = '111111'
            assertTrueMethod(msg, data['expect'])
            # assertTrueMethod(msg, data['expect'])

            logger.info(" 结束执行 {0} 测试用例， 测试结果 --- PASS ".format(sys._getframe().f_code.co_name))
            LoginPage(start_session).save_screenshot("正常截图")
        except:
            logger.error(" 结束执行 {0} 测试用例， 测试结果 --- False ".format(sys._getframe().f_code.co_name))
            LoginPage(start_session).save_screenshot("异常截图")
            raise

    # 正常用例
    # @pytest.mark.lucas
    # @pytest.mark.smoke
    # @pytest.mark.parametrize('data', pass_data)
    # def test_login_success(self, data, start_session):
    #     logger.info(" 执行 {0} 测试套件Suite ".format(self.__class__.__name__))
    #     logger.info(" 执行 {0} 测试用例Case ".format(sys._getframe().f_code.co_name))
    #     LoginPage(start_session).input_username(data['user'])
    #     LoginPage(start_session).input_pwd(data['pwd'])
    #     LoginPage(start_session).login_btn()
    #
    #     try:
    #         assert IndexPage(start_session[0]).isExist_logout_ele()
    #         logger.info(" 结束执行 {0} 测试用例， 测试结果 --- PASS ".format(sys._getframe().f_code.co_name))
    #         start_session[1].save_pictuer("{0}-正常截图".format(LD.success_data['name']))
    #     except:
    #         logger.error(" 结束执行 {0} 测试用例， 测试结果 --- False ".format(sys._getframe().f_code.co_name))
    #         start_session[1].save_pictuer("{0}-异常截图".format(LD.success_data['name']))
    #         raise
