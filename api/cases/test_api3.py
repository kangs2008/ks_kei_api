import pytest
import allure
import sys, os
from Common.handle_logger import logger
from api.apikeywords.apiKeyWords3 import Http
from Common.excel_api import excel_to_case, load_excel, excel_to_save, write_to_excel3, Handle_excel
from Common.handle_config2 import ReadWriteConfFile
from Common.setting import REPORT_DIR

execfile = ReadWriteConfFile().get_option('exec', 'exec_file_path')
execfolder = ReadWriteConfFile().get_option('exec', 'exec_current_folder')
execsheet = ReadWriteConfFile().get_option('exec', 'exec_sheet_name')

report_excel = ReadWriteConfFile().get_option('report_dir2', 'report_dir_folder')
tmp_excel_path = os.path.join(REPORT_DIR, report_excel)


apidata = excel_to_case(execfile, execfolder, execsheet)
print('apidata::::', apidata)



# @pytest.mark.usefixtures('start_session')
# @pytest.mark.usefixtures('refresh_page')
# @allure.feature('API测试')
class TestAPI():

    @pytest.mark.parametrize('data', apidata)
    def test_all_api(self, requests_session, data):

        http = Http(requests_session)

        allure.dynamic.feature(f'API测试')
        allure.dynamic.story(f'{list(data.values())[1]}||{list(data.values())[0]}')
        allure.dynamic.description(f'FILE SHEET： {list(data.values())[0]}  \n\nFILE NAME： {list(data.values())[1]}  \n\nFILE PATH： {list(data.values())[2]}')
        wb, sheet, write_path = self.load_excel_setup(list(data.values())[0], list(data.values())[1], list(data.values())[2])

        exec_c, col_pos_c = Handle_excel(list(data.values())[2]).getColumnValuesByTitle(sheet, 'return_code')
        exec_v, col_pos_v = Handle_excel(list(data.values())[2]).getColumnValuesByTitle(sheet, 'return_values')

        logger.info(f"执行测试套件: {self.__class__.__name__}")
        logger.info(f"执行测试用例: {list(data.values())[0]}")

        for va in list(data.values())[3]:

            self.allurestep(va) # tilte only
            self.__t_data(va)

            # if hasattr(http, va['method']):
            #     logger.info("aaaaaaaaaaaaaaaaaaaaaaaa")
            # else:
            #     logger.info("bbbbbbbbbbbbbbbbbbbbbbbb")

            func = getattr(http, va['method'])
            row_pos = va['exec']
            res = func(va, sheet, row_pos, col_pos_c, col_pos_v)

            logger.info(f'函数返回值：{str(res)}')


            # write_to_excel(sheet, str(res), write_pos)
            # write_to_excel3(sheet, str(res), row_pos, col_pos_c)
            # write_to_excel3(sheet, str(res), row_pos, col_pos_v)

        self.save_excel_teardown(wb, write_path)

        logger.info(f"写入Excel：{'save_excel_teardown'}")

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
        write_file_name = os.path.splitext(file_name)[0] + '_report' + os.path.splitext(file_name)[1]
        new_path = file_path.replace(file_path, tmp_excel_path)
        write_file_path = os.path.join(new_path, write_file_name)

        wb, sheet = load_excel(write_file_path, sheet_name)
        return wb, sheet, write_file_path

    def save_excel_teardown(self, wb, file_path):
        excel_to_save(wb, file_path)
