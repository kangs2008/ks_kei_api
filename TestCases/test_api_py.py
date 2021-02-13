import pytest
import allure
import sys, os
from Common.handle_logger import logger
from Apikeywords.apiKeyWords import Http
from Common.handle_excel import excel_to_case, load_excel, excel_to_save, Handle_excel
from Common.handle_config import ReadWriteConfFile
from Common.setting import REPORT_DIR, DATAS_DIR


execsheet = ReadWriteConfFile().get_option('exec', 'exec_sheet_name')
report_excel = ReadWriteConfFile().get_option('report_dir', 'report_dir_folder')
tmp_excel_path = os.path.join(REPORT_DIR, report_excel)
# report_excel_name = ReadWriteConfFile().get_option('report_file', 'report_file_name')
num = ReadWriteConfFile().get_option('report_file', 'file_num')

execfile = os.path.join(DATAS_DIR, 'test_apidata.xlsx')
sheet_name = 't_接口py'

apidata = excel_to_case(execfile, '', sheet_name)
apidata_length = len(apidata)
print('::::::::::::apidata::::::::::::', apidata)

test_data = ''
test_sheet_name = ''
test_file_name = ''
test_file_name = ''
if execfile == '' and apidata_length > 1:
    raise Exception('请指定测试 sheet 名称')
elif execfile == '' and apidata_length == 1:
    test_data = apidata[0]['filesheet']
    test_sheet_name = apidata[0]['sheetname']
    test_file_name = apidata[0]['file']
    test_file_path = apidata[0]['filepath']
else:
    for data_ in apidata:
        if data_['sheetname'] == execsheet:
            test_data = data_['filesheet']
            test_sheet_name = data_['sheetname']
            test_file_name = data_['file']
            test_file_path = data_['filepath']

if test_data == '':
    raise Exception('请检查测试数据是否正确')



# @pytest.mark.usefixtures('start_session')
# @pytest.mark.usefixtures('refresh_page')
# @allure.feature('API测试')
class TestXXX():

    @pytest.mark.parametrize('data', test_data)
    def test_all_api(self, requests_session, data):

        http = Http(requests_session)
        try:
            allure.dynamic.feature(f'{self.__class__.__name__}')
            allure.dynamic.story(f'{test_sheet_name}')
            allure.dynamic.description(f'FILE SHEET： {test_sheet_name}  \n\nFILE NAME： {test_file_name}  \n\nFILE PATH： {test_file_path}')
            logger.info(f'API测试')
            logger.info(f'FILE SHEET： {test_sheet_name}  FILE NAME： {test_file_name}  FILE PATH： {test_file_path}')

            wb, sheet, write_path = self.load_excel_setup(test_sheet_name, test_file_name, test_file_path)

            exec_c, col_pos_c = Handle_excel(test_file_path).getColumnValuesByTitle(sheet, 'return_code')
            exec_v, col_pos_v = Handle_excel(test_file_path).getColumnValuesByTitle(sheet, 'return_values')

            logger.info(f"执行测试套件: {sys._getframe().f_code.co_name}")
            logger.info(f"执行测试用例: {test_sheet_name}")

            http.py_get(data, sheet, data['exec'], col_pos_c, col_pos_v)
            self.save_excel_teardown(wb, write_path)
            logger.info(f"写入Excel：{'save_excel_teardown'}")
        except Exception as e:
            logger.info(f"ERROR METHOD：{sys._getframe().f_code.co_name}")
            logger.error(e)
            raise

    def allurestep(self, va):
        if va['title'] != '':
            with allure.step(f"测试功能是：{va['title']}"):
                logger.info(f"测试功能是：{va['title']}")

    def __t_data(self, va):
        title = ''
        method = ''
        input = ''
        request_data = ''
        status = ''

        if va['title'] != '':
            title = va['title']
        if va['method'] != '':
            method = va['method']
        if va['input'] != '':
            input = va['input']
        if va['request_data'] != '':
            request_data = va['request_data']
        logger.info(f"测试数据是:【title:[{title}], method:[{method}], input:[{input}], request_data:[{request_data}]】")

    def load_excel_setup(self, sheet_name, file_name, file_path):
        # write_file_name = os.path.splitext(file_name)[0] + '_report' + os.path.splitext(file_name)[1]
        if num == '':
            numstr = ''
        else:
            numstr = f'(' + num + ')'
        write_file_name = os.path.splitext(file_name)[0] + '_report' + numstr + os.path.splitext(file_name)[1]
        new_path = file_path.replace(file_path, tmp_excel_path)
        write_file_path = os.path.join(new_path, write_file_name)

        wb, sheet = load_excel(write_file_path, sheet_name)
        return wb, sheet, write_file_path

    def save_excel_teardown(self, wb, file_path):
        excel_to_save(wb, file_path)

    def __to_list(self, file_str, name):
        fileList = str(file_str).split(',')
        for one in fileList:
            pre = os.path.splitext(one)[0]
            if pre in name:
                return name