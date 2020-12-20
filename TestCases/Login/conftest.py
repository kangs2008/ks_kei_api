import pytest
import os
import sys
from time import sleep
from selenium import webdriver
from Datas.global_datas import base_usl
from Pages import LoginPage
from Common.basepage import BasePage
from Common.handle_logger import logger

driver = None

@pytest.fixture(scope='class')
def start_module(project_module_start):
    '''
    每个模块单独打开一次浏览器，此时 driver.quit() 需要单独加上
    :param project_module_start:  每个模块单独打开一次浏览器
    :return: driver lg
    '''
    logger.info("==========开始执行测试用例集===========")
    global driver
    driver = project_module_start
    driver.get(base_usl)
    # lg = LoginPage(driver)
    # yield (driver, lg)
    yield driver
    logger.info("==========结束执行测试用例集===========")
    # driver.quit()


@pytest.fixture(scope='class')
def start_session(project_session_start):
    '''
    所有模块只打开一次浏览器
    :param project_session_start: 所有模块只打开一次浏览器
    :return: driver lg
    '''
    logger.info("==========开始执行测试用例集===========")
    global driver
    driver = project_session_start
    logger.info("----------------------------------------------------------------------------------" + str(driver))
    driver.get(base_usl)
    # lg = LoginPage(driver)
    # yield (driver, lg)
    yield driver
    logger.info("==========结束执行测试用例集===========")


@pytest.fixture()
def refresh_page():
    yield
    driver.refresh()
    sleep(3)
