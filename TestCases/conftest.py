import pytest
import os
import sys
from selenium import webdriver
from Common.handle_logger import logger
from Common.setting import *

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print(BASE_DIR)

driver = None


@pytest.fixture(scope='session')
def project_session_start():
    logger.info("==========开始 XX项目 执行测试===========")
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
    logger.info("==========结束 XX项目 测试===========")


@pytest.fixture(scope='module')
def project_module_start():
    logger.info("==========开始 XX模块 执行测试===========")
    global driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()
    logger.info("==========结束 XX模块 测试===========")


@pytest.fixture()
def project_func():
    print("project_func")

