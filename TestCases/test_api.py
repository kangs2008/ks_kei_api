import pytest
import allure
import os, sys
from Common.handle_logger import logger
from Apikeywords.apiKeyWords import Http
from Common.handle_excel import excel_to_case, load_excel, excel_to_save, Handle_excel
from Common.handle_config import ReadWriteConfFile
from Common.setting import REPORT_DIR, BASE_DIR

execfile = ReadWriteConfFile().get_option('exec', 'exec_file_path')
execst = ReadWriteConfFile().get_option('exec', 'st')
execsheet = ReadWriteConfFile().get_option('exec', 'exec_sheet_name')

report_excel = ReadWriteConfFile().get_option('report_dir', 'report_dir_folder')
tmp_excel_path = os.path.join(REPORT_DIR, report_excel)
num = ReadWriteConfFile().get_option('report_file', 'file_num')

apidata = excel_to_case(execfile, execst, execsheet)

class TestAPI():

    @pytest.mark.parametrize('data', apidata)
    def test_all_api(self, requests_session, data):

        http = Http(requests_session)

        allure.dynamic.feature(f'API_interface_test')
        allure.dynamic.story(f'{list(data.values())[1]}<>{list(data.values())[0]}')
        allure.dynamic.description(f'FILE SHEET： {list(data.values())[0]}  \n\nFILE NAME： {list(data.values())[1]}  \n\nFILE PATH： {list(data.values())[2]}')
        logger.info(f'API_interface_test')
        logger.info(f'FILE SHEET： {list(data.values())[0]}  FILE NAME： {list(data.values())[1]}  FILE PATH： {list(data.values())[2]}')
        logger.info(list(data.values())[2])
        wb, sheet, write_path = self.load_excel_setup(list(data.values())[0], list(data.values())[1], list(data.values())[2])

        exec_c, col_pos_c = Handle_excel(list(data.values())[2]).getColumnValuesByTitle(sheet, 'return_code')
        exec_v, col_pos_v = Handle_excel(list(data.values())[2]).getColumnValuesByTitle(sheet, 'return_values')

        logger.info(f"Execute test suite: {self.__class__.__name__}")
        logger.info(f"Execute test case: {list(data.values())[0]}")

        for va in list(data.values())[3]:

            self.allurestep(va) # tilte only
            self.__t_data(va)

            func = getattr(http, va['method'])
            row_pos = va['exec']
            res = func(va, sheet, row_pos, col_pos_c, col_pos_v)

            logger.info(f'Function return value：{str(res)}')

        self.save_excel_teardown(wb, write_path)

        logger.info(f"Write Excel：{'save_excel_teardown'}")

    def allurestep(self, va):
        if va['title'] != '':
            with allure.step(f"Test title：{va['title']}"):
                logger.info(f"Test title：{va['title']}")

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
        logger.info(f"Test datas:【title:[{title}], method:[{method}], input:[{input}], request_data:[{request_data}]】")

    def load_excel_setup(self, sheet_name, file_name, file_path):
        if num == '':
            numstr = ''
        else:
            numstr = f'(' + num + ')'
        p = self._re_file_path(file_path)
        write_file_name = os.path.splitext(file_name)[0] + '_report' + numstr + os.path.splitext(file_name)[1]
        new_path = file_path.replace(file_path, tmp_excel_path)

        if p:
            new_path = new_path + p

        write_file_path = os.path.join(new_path, write_file_name)
        logger.info(f'aaaaaaaa{write_file_path}')
        wb, sheet = load_excel(write_file_path, sheet_name)
        return wb, sheet, write_file_path
    def _re_file_path(self, file_path):
        datas_path = os.path.join(BASE_DIR, "Datas")
        logger.info(file_path)
        logger.info(datas_path)
        logger.info('datas_path')
        if sys.platform == 'win32':
            new_report_path = file_path.replace(datas_path.replace('\\', '/'), '')
            # p, f = os.path.split(new_report_path.replace('/', '\\'))
            p, f = os.path.split(new_report_path)
        else:
            new_report_path = file_path.replace(datas_path, '')
            p, f = os.path.split(new_report_path)
        return p

    def save_excel_teardown(self, wb, file_path):
        excel_to_save(wb, file_path)

    def __to_list(self, file_str, name):
        fileList = str(file_str).split(',')
        for one in fileList:
            pre = os.path.splitext(one)[0]
            if pre in name:
                return name
