import os, re
import click
import pytest
import time

from Common.handle_config2 import ReadWriteConfFile
from Common.utils import start_time_format, use_time, report_date_folder
from Common.handle_file import file_del, file_zip_path, file_copy, file_and_folder_copy
from Common.setting import BASE_DIR, REPORT_DIR

def set_exec_usefile(file, folder, sheet):
    if os.path.isdir(file) or os.path.isfile(file): # dir or file
        ReadWriteConfFile().set_option('exec', 'exec_file_path', file)
        if folder:
            ReadWriteConfFile().set_option('exec', 'exec_current_folder', str(folder))
        else:
            ReadWriteConfFile().set_option('exec', 'exec_current_folder', '')
        if sheet:
            ReadWriteConfFile().set_option('exec', 'exec_sheet_name', str(sheet))
        else:
            ReadWriteConfFile().set_option('exec', 'exec_sheet_name', '')
        if os.path.isfile(file):
            return True
    else: # error file or floder
        ReadWriteConfFile().set_option('exec', 'exec_file_path', '')
        ReadWriteConfFile().set_option('exec', 'exec_current_folder', '')
        ReadWriteConfFile().set_option('exec', 'exec_sheet_name', '')
    return False

def set_exec_ini(section, option, value):
    ReadWriteConfFile().add_section(section)
    ReadWriteConfFile().set_option(section, option, value)
def html_num(fileName):
    pre = os.path.splitext(fileName)[0]
    pattern = re.findall('[(](.*?)[)]', pre)
    print(pattern)
    if pattern:
        return str('(' + pattern[0] + ')')
    else:
        return ''

datas_path = os.path.join(BASE_DIR, "Datas")
datas_path_file = os.path.join(datas_path, "test_apidata.xlsx")

@click.command()
@click.option('--file', default=datas_path, help='指定文件名字:datas_path_file or 文件夹:datas_path')
@click.option('--sheet', default=None, help='None 指定文件 sheet name, 默认遍历文件里所有 sheet name')
@click.option('--folder', default=None, help='None 输入任意字符，表示遍历文件和文件夹')
@click.option('--report', default=report_date_folder, help='当天日期为报告文件夹：2020-12-19  or None')
def main(file, folder, sheet, report):
    starttime = time.time()
    if report is None:
        report_dir_format = start_time_format(starttime) + '_allure'
        set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
        st = set_exec_usefile(file, folder, sheet)
        file_del(os.path.join(BASE_DIR, 'temp'))
        mk_report_dir = os.path.join(REPORT_DIR, report_dir_format)
        os.mkdir(mk_report_dir)
    else:
        report_dir_format = report + '_allure'
        set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
        st = set_exec_usefile(file, folder, sheet)
        file_del(os.path.join(BASE_DIR, 'temp'))
        mk_report_dir = os.path.join(REPORT_DIR, report_dir_format)
        print(mk_report_dir)
        if not os.path.exists(mk_report_dir):
            os.mkdir(mk_report_dir)

    if st:
        print('11111')
        new_report_excel_name = file_copy(datas_path, 'test_apidata.xlsx', f'test_apidata.xlsx', f'{mk_report_dir}', 're_name')
    else:
        print('2222')
        new_report_excel_name = file_and_folder_copy(datas_path, f'{mk_report_dir}', ['test_'], 're_name')
    print(new_report_excel_name)
    set_exec_ini('report_file', 'report_file_name', new_report_excel_name)
    num = html_num(new_report_excel_name)
    set_exec_ini('report_file', 'file_num', num)

    from Common.handle_logger import logger
    logger.info(f'----------传入参数<--file>,测试excel：{file}')
    logger.info(f'----------传入参数<--sheet>,测试excel sheet name：{sheet}')
    logger.info(f'----------传入参数<--folder>,测试文件或文件夹的文件：{folder}')
    logger.info(f'----------传入参数<--report>,指定测试报告文件夹：{report}_allure')

    logger.info(f'测试报告文件夹：{os.path.join(REPORT_DIR, report_dir_format)}')

    # pytest.main(['-sv', './TestCases/Login/test_login.py', '--alluredir', './temp']) # web test




    pytest.main(['-sv', './api/cases/test_api4.py', '--alluredir', './temp']) # api test
    os.system(f'allure generate ./temp -o ./Report/{report_dir_format}/allure/ --clean')
    time.sleep(3)




    input_path = os.path.join(REPORT_DIR, report_dir_format)
    output_path = os.path.join(REPORT_DIR, f'{report_dir_format}_{num}.zip')
    print('zip')
    file_zip_path(input_path, output_path, ignore=[]) # 压缩文件
    logger.info(f'测试报告压缩路径：{output_path}')

    endtime = time.time()
    logger.info(use_time(starttime, endtime))
    set_exec_ini('report_file', 'file_num', '')

if __name__ == '__main__':
    main()

    pass