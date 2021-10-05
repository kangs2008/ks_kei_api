import pytest, os, subprocess
from Common.handle_config import ReadWriteConfFile
from conftest import set_exec_ini
from Common.setting import BASE_DIR


file_path = r"D:/desk20201127/ksgit/TestCases/" #test_apidata.xlsx
# datas_path = os.path.join(BASE_DIR, "Datas")


set_exec_ini('exec', 'exec_file_path', file_path)
set_exec_ini('exec', 'exec_sheet_name', '')

pytest.main([])  # '--report','re2021'
dir = ReadWriteConfFile().get_option('report_dir', 'report_dir_folder')
cmd = f'allure generate ./temp -o ./Report/{dir}/allure/ --clean'
# report_dir_format = ReadWriteConfFile().set_option('report_dir', 'report_dir_folder', '')
os.system(cmd)

# execfile = os.path.join(os.path.dirname(__file__),'a.py') #D:/desk20201127/ksgit\a.py
# print(execfile)
