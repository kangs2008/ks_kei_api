# -*- coding: utf-8 -*-

import pytest
import allure
import requests
from Common.handle_logger import logger

_session = None

@pytest.fixture(scope="function", autouse=True)
def requests_session():
    """
    init requests.session()
    """
    logger.info('*'*100)
    logger.info('*'*20 + '测试执行开始' + '*'*20)
    global _session
    _session = requests.session()
    # allure.step(f'获取session：{_session}')
    logger.info(f'----------requests_session setup----------')
    logger.info(f'获取session：{_session}')
    yield _session
    _session.close()
    logger.info(f'销毁session：{_session}')
    logger.info(f'----------requests_session teardown----------')
    # allure.environment(test_platform=host["test_platform"])
    # allure.environment(mock=host["mock"])
    logger.info('*'*20 + '测试执行结束' + '*'*20)
    logger.info('*' * 100)

