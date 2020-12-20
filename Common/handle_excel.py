from openpyxl import load_workbook
from Common.handle_config import HandleConfig
from Common.setting import DATAS_FILE_PATH
# actual_col = conf.get_int("message", "actual_col")
# result_col = conf.get_int("message", "result_col")


class HandleExcel:
    '''
    定义一个文件处理类
    '''
    def __init__(self, filename, sheet_name=None):
        self.filename = filename  # 文件名
        self.sheet_name = sheet_name  # 表单名

    def get_cases(self):  # 获取所有的测试用例
        wb = load_workbook(self.filename)
        if self.sheet_name is None:  # 是否指定一个表单
            ws = wb.active
        else:
            ws = wb[self.sheet_name]
        header_info = tuple(ws.iter_rows(max_row=1, values_only=True))[0]
        cases_dict = []
        for one_case in tuple(ws.iter_rows(min_row=2, values_only=True)):
            cases_dict.append(dict(zip(header_info, one_case)))
        wb.close()
        return cases_dict

    def get_one_case(self, row):  # 获取某一条测试用例
        return self.get_cases()[row-1]

    def write_case(self, row, write_actual, write_result):  # 写入数据到测试用例中
        wb = load_workbook(self.filename)
        if self.sheet_name is None:
            ws = wb.active
        else:
            ws = wb[self.sheet_name]
        if row >= 2:  # 这里限制不能修改表头信息
            ws.cell(row=row, column=0, value=write_actual)
            ws.cell(row=row, column=0, value=write_result)
        else:
            print("输入行号有误！")
        wb.save(self.filename)
        wb.close()


case_path = DATAS_FILE_PATH  # 获取测试用例文件名

# xxx_sheet_name = conf.get_value("file_path", "xxx_sheet_name")  # 获取表单名
# xxx_handle_case = HandleExcel(case_path, xxx_sheet_name)
# xxx_cases = xxx_handle_case.get_cases()  # 获取对应表单的所有测试用例