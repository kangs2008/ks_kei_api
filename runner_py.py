import os
import click
import re
import time

from Common.handle_config import ReadWriteConfFile
from Common.utils import start_time_format, use_time, report_date_folder
from Common.handle_file import file_del, current_folder_file_copy
from Common.setting import BASE_DIR, REPORT_DIR

datas_path = os.path.join(BASE_DIR, "Datas")

@click.command()
@click.option('--report', default=report_date_folder, help='当天日期为报告文件夹：2020-12-19  or None')
def main(report):
    starttime = time.time()
    set_exec_ini('report_file', 'file_num', '')
    if report is None:
        report_dir_format = start_time_format(starttime) + '_html'
        set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
        st = set_exec_usefile()
        file_del(os.path.join(BASE_DIR, 'temp'))
        mk_report_dir = os.path.join(REPORT_DIR, report_dir_format)
        os.mkdir(mk_report_dir)
    else:
        report_dir_format = report + '_html'
        set_exec_ini('report_dir', 'report_dir_folder', report_dir_format)
        st = set_exec_usefile()
        file_del(os.path.join(BASE_DIR, 'temp'))
        mk_report_dir = os.path.join(REPORT_DIR, report_dir_format)
        if not os.path.exists(mk_report_dir):
            os.mkdir(mk_report_dir)
    set_exec_ini('exec', 'st', st)
    set_exec_ini('report_dir', 'py_report_dir_folder', mk_report_dir)

    # new_report_excel_name = current_folder_file_copy(datas_path, f'{mk_report_dir}', ['test_', '.xlsx'], 're_name')
    # set_exec_ini('report_file', 'report_file_name', new_report_excel_name)
    # num = html_num(new_report_excel_name)
    # set_exec_ini('report_file', 'file_num', num)







    from Common.handle_logger import logger

    logger.info(f'----------传入参数<--report>,指定测试报告文件夹：{report}')

    logger.info(f'测试报告文件夹：{mk_report_dir}') # os.path.join(REPORT_DIR, report_dir_format)

    os.system(f'cd {BASE_DIR}')
    num = ReadWriteConfFile().get_option('report_file', 'file_num')
    os.system(f'pytest {BASE_DIR}/TestCases/test_api_py.py -v --html={BASE_DIR}/Report/{report_dir_format}/{report_dir_format}_report_{num}_.html --self-contained-html')

    # input_path = os.path.join(REPORT_DIR, report_dir_format)
    # output_path = os.path.join(REPORT_DIR, f'{report_dir_format}.zip')
    # file_zip_path(input_path, output_path, ignore=[]) # 压缩文件
    # logger.info(f'测试报告压缩路径：{output_path}')


    endtime = time.time()
    logger.info(use_time(starttime, endtime))
    set_exec_ini('report_file', 'file_num', '')

def set_exec_usefile():
    ReadWriteConfFile().set_option('exec', 'exec_file_path', datas_path)
    ReadWriteConfFile().set_option('exec', 'exec_sheet_name', '')
    return '1'

def set_exec_ini(section, option, value):
    ReadWriteConfFile().add_section(section)
    ReadWriteConfFile().set_option(section, option, value)
def html_num(fileName):
    pre = os.path.splitext(fileName)[0]
    pattern = re.findall('[(](.*?)[)]', pre)
    if pattern:
        return str(pattern[0])
    else:
        return ''
if __name__ == '__main__':
    main()

