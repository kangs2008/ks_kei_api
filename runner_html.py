import os
import click
import pytest
import time

from Common.handle_config2 import ReadWriteConfFile
from Common.utils import start_time_format, use_time
from Common.handle_file import file_del, file_zip_path, file_copy, file_and_folder_copy
from Common.setting import BASE_DIR, REPORT_DIR

def set_exec_usefile(file, folder, sheet):
    if os.path.isdir(file) or os.path.isfile(file):  # dir or file
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
    else:  # error file or floder
        ReadWriteConfFile().set_option('exec', 'exec_file_path', '')
        ReadWriteConfFile().set_option('exec', 'exec_current_folder', '')
        ReadWriteConfFile().set_option('exec', 'exec_sheet_name', '')
    return False

def set_exec_logdir(to_time):
    ReadWriteConfFile().add_section('report_dir')
    ReadWriteConfFile().set_option('report_dir', 'report_dir_folder', to_time)

datas_path = os.path.join(BASE_DIR, "Datas")
datas_path_file = os.path.join(datas_path, "test_apidata.xlsx")

@click.command()
@click.option('--file', default=datas_path_file, help='指定文件名字 or 文件夹:datas_path')
@click.option('--sheet', default=None, help='None 指定文件 sheet name, 默认遍历文件里所有 sheet name')
@click.option('--folder', default=None, help='None 输入任意字符，表示遍历文件和文件夹')
def main(file, folder, sheet):
    starttime = time.time()
    report_dir_format = start_time_format(starttime)
    set_exec_logdir(report_dir_format)
    st = set_exec_usefile(file, folder, sheet)

    file_del(os.path.join(BASE_DIR, 'temp'))
    mk_report_dir = os.path.join(REPORT_DIR, report_dir_format)
    os.mkdir(mk_report_dir)

    if st:
        print('11111')
        file_copy(datas_path, 'test_apidata.xlsx', f'test_apidata.xlsx', r'D:\desk20201127\ks\Report\2020-12-09_21-08-17', 're_name')
    else:
        print('2222')
        file_and_folder_copy(datas_path, r'D:\desk20201127\ks\Report\2020-12-09_21-08-17', ['test_'], 're_name')





    from Common.handle_logger import logger

    logger.info(f'----------传入参数<--file>,测试excel：{file}')
    logger.info(f'----------传入参数<--sheet>,测试excel sheet name：{sheet}')
    logger.info(f'----------传入参数<--folder>,测试文件或文件夹的文件：{folder}')


    logger.info(f'测试报告文件夹：{mk_report_dir}') # os.path.join(REPORT_DIR, report_dir_format)

    os.system(f'cd {BASE_DIR}')
    # os.system(f'pytest {BASE_DIR}/api/cases/test_api.py --html={BASE_DIR}/Reports/{report_dir_format}_report.html --self-contained-html')
    os.system(f'pytest {BASE_DIR}/api/cases/test_api3.py --html={BASE_DIR}/Reports/{report_dir_format}_report.html --self-contained-html')

    # input_path = os.path.join(REPORT_DIR, report_dir_format)
    # output_path = os.path.join(REPORT_DIR, f'{report_dir_format}.zip')
    # file_zip_path(input_path, output_path, ignore=[]) # 压缩文件
    # logger.info(f'测试报告压缩路径：{output_path}')


    endtime = time.time()
    logger.info(use_time(starttime, endtime))

if __name__ == '__main__':
    main()
    # python runner_html.py --folder 1

