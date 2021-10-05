# -*- coding: utf-8 -*-
import pytest, os, time, subprocess, sys, re
import requests
from Common.handle_logger import logger
from Common.handle_config import ReadWriteConfFile
from Common.utils import start_time_format, use_time, report_date_folder
from Common.handle_file import file_zip_path, file_del, file_copy, file_and_folder_copy, current_folder_file_copy
from Common.setting import BASE_DIR, REPORT_DIR, REPORT_CURRENT_DIR
from Common.handle_logger import logger


_session = None
_date = report_date_folder()
datas_path = os.path.join(BASE_DIR, "TestCases")
sheet = ReadWriteConfFile().get_option('exec', 'exec_sheet_name')
file_name = "test_apidata.xlsx"
execfile = ReadWriteConfFile().get_option('exec', 'exec_file_path')


def pytest_addoption(parser):
    """add --report"""
    parser.addoption(
        "--report",
        action="store",
        default=_date,  # 'Report_allure'
        help="current report directory"
    )


@pytest.fixture(scope="session", autouse=True)
def report(request):
    """get command line parameters
    :param request: --report
    """
    starttime = time.time()
    set_exec_ini('report_file', 'file_num', '')
    set_exec_ini('report_dir', 'report_dir_folder', '')

    if request.config.getoption("--report") is None or request.config.getoption("--report") =='':
        report_dir_format = start_time_format(starttime) + '_allure'
        set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
        st = set_exec_usefile(datas_path, sheet)
        # file_del(os.path.join(BASE_DIR, 'temp'))

        mk_report_dir = os.path.join(REPORT_DIR, report_dir_format)
        logger.info(f'-----mk_report_dir--：{mk_report_dir}')
        os.mkdir(mk_report_dir)
        set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
    else:
        report_dir_format = request.config.getoption("--report") + '_allure'
        set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
        st = set_exec_usefile(datas_path, sheet)
        # file_del(os.path.join(BASE_DIR, 'temp'))
        mk_report_dir = os.path.join(REPORT_DIR, report_dir_format)
        logger.info(f'-----mk_report_dir--：{mk_report_dir}')
        if not os.path.exists(mk_report_dir):
            logger.info(f'-----mk_report_dir-')
            os.mkdir(mk_report_dir)
        set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)

    set_exec_ini('exec', 'st', st)

    if st == '1':
        print('11')
        new_report_excel_name = file_copy(datas_path, execfile, execfile, f'{mk_report_dir}', 're_name')
    elif st == '2':
        print('22')
        new_report_excel_name = current_folder_file_copy(datas_path, f'{mk_report_dir}', ['test_', '.xlsx'], 're_name')
    else:
        print('33')
        new_report_excel_name = file_and_folder_copy(datas_path, f'{mk_report_dir}', ['test_', '.xlsx'], 're_name')
    set_exec_ini('report_file', 'report_file_name', new_report_excel_name)
    num = html_num(new_report_excel_name)
    set_exec_ini('report_file', 'file_num', num)

    # from Common.handle_logger import logger
    logger.info(f'----------传入参数<--file>,测试excel：{execfile}')
    logger.info(f'----------传入参数<--sheet>,测试excel sheet name：{sheet}')
    logger.info(f'----------传入参数<--report>,指定测试报告文件夹：{request.config.getoption("--report")}_allure')

    logger.info(f'测试报告文件夹：{os.path.join(REPORT_DIR, report_dir_format)}')




    yield request.config.getoption("--report")

    input_path = os.path.join(REPORT_DIR, report_dir_format)
    output_path = os.path.join(REPORT_DIR, f'{report_dir_format}_{num}.zip')
    file_zip_path(input_path, output_path, ignore=[])  # 压缩文件
    logger.info(f'测试报告压缩路径：{output_path}')
    set_exec_ini('report_file', 'file_num', '')

    # set_exec_ini('report_dir', 'report_dir_folder', '')
    set_exec_ini('exec', 'exec_sheet_name', '')

    endtime = time.time()
    logger.info(f"------------------------")
    logger.info(use_time(starttime, endtime))
    logger.info(f"------------------------")


def set_exec_ini(section, option, value):
    ReadWriteConfFile().add_section(section)
    ReadWriteConfFile().set_option(section, option, value)
def set_exec_usefile(_file, sheet):
    if os.path.isfile(_file):  # dir or file
        datas_path_file = os.path.join(datas_path, _file)
        logger.info(f"---datas_path:{datas_path}-------{datas_path_file}--------------")
        ReadWriteConfFile().set_option('exec', 'exec_file_path', datas_path_file)
        if sheet:
            ReadWriteConfFile().set_option('exec', 'exec_sheet_name', str(sheet))
        else:
            ReadWriteConfFile().set_option('exec', 'exec_sheet_name', '')
        return '1'
    elif os.path.isdir(_file):  # dir or file
        ReadWriteConfFile().set_option('exec', 'exec_file_path', _file)
        if sheet:
            ReadWriteConfFile().set_option('exec', 'exec_sheet_name', str(sheet))
        else:
            ReadWriteConfFile().set_option('exec', 'exec_sheet_name', '')
        return '2'
    else:  # error file or floder
        logger.info(f"---datas_path:{datas_path}---------------------")
        ReadWriteConfFile().set_option('exec', 'exec_file_path', datas_path)
        ReadWriteConfFile().set_option('exec', 'exec_sheet_name', '')
        return '3'

def html_num(fileName):
    pre = os.path.splitext(fileName)[0]
    pattern = re.findall('[(](.*?)[)]', pre)
    if pattern:
        return str(pattern[0])
    else:
        return ''


@pytest.fixture(scope="function", autouse=True)
def requests_session():
    """
    init requests.session()
    """
    logger.info('*'*100)
    logger.info('*'*20 + '测试执行开始' + '*'*20)
    global _session
    _session = requests.session()
    logger.info(f'----------requests_session setup----------')
    logger.info(f'获取session：{_session}')
    yield _session
    _session.close()
    logger.info(f'销毁session：{_session}')
    logger.info(f'----------requests_session teardown----------')
    logger.info('*'*20 + '测试执行结束' + '*'*20)
    logger.info('*' * 100)

