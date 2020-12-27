import time
import os, sys
import pytest
from Common.handle_config2 import ReadWriteConfFile
from Common.utils import start_time_format, use_time
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
def set_exec_logdir(to_time):
    ReadWriteConfFile().add_section('report_dir')
    ReadWriteConfFile().set_option('report_dir', 'report_dir_folder', to_time)

datas_path = os.path.join(BASE_DIR, "Datas")

starttime = time.time()
report_dir_format = start_time_format(starttime)
set_exec_logdir(report_dir_format)

file = r'--file=D:\desk20201127\ks\Datas\test_apidata.xlsx'

# pytest.main(['-sv', f'{file}', '--sheet=t_接', '--folder=None', './api/cases/test_api3.py'])

pytest.main(['-sv', './api/cases/test_api3.py'])

set_exec_usefile(file, folder, sheet)