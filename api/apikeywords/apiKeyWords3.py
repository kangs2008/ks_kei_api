import json, sys
import re
import allure
import jsonpath
from Common.utils import mTime
from Common.handle_logger import logger
from Common.excel_api import excel_to_case, load_excel, excel_to_save, write_to_excel3
class Http():

    def __init__(self, requests_session):
        self.url = ''
        self.result = None
        self.jsonres = {}
        self.session = requests_session
        self.relations = {}


        self.h1 = {"X-Lemonban-Media-Type": "lemonban.v2"}
        self.h2 = {"Content-Type": "application/json"}

    def __hander_henders(token=None):
        headers = {"X-Lemonban-Media-Type": "lemonban.v2",
                   "Content-Type": "application/json"}
        if token:
            headers["Authorization"] = "Bearer {}".format(token)
        return headers

    def __get_relations(self, param):
        if param is None or param == '':
            return None
        else:
            for key in self.relations:
                param = param.replace('{' + key + '}', self.relations[key])
            return param
    def __get_data(self, param):
        # if (param is not None or param != '') and isinstance(param, str):
        #     return json.loads(param)  # 用于将str类型的数据转成dict
        # else:
        #     return None

        if (param is None) or param == '':
            return None
        else:
            # p = {}
            # params = param.split('&')
            # for s in params:
            #     if s == '':
            #         pass
            #     else:
            #         key = s[:s.find('=')]
            #         value = s[s.find('=') + 1 :]
            #         p[key] = value
            # return p
            return json.loads(param) # 用于将str类型的数据转成dict

    def __allurestep(self, str_fail='FAIL'):
        if str_fail == 'FAIL':
            with allure.step(f"对比结果：{str_fail}"):
                pass

    def __abs(self, datan):
        dataL = datan.split(',')
        tmp = ''
        for one in dataL:
            if one.strip().isdigit():
                tmp = tmp + f"[{one.strip()}]"
            else:
                tmp = tmp + f"['{one.strip()}']"
        return tmp

    def assertJsonpath(self, data, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
        expect_value = str(data['request_data']).strip()
        datan = str(data['input']).strip()
        result_to_json = json.dumps(self.jsonres)
        res = jsonpath.jsonpath(result_to_json, f'$..{datan}')  # 找不到是结果是 False
        with allure.step(
                f"[{mTime()}]['assertInRe'][key:{datan},actual_value:{res}][expect_value:{expect_value}]"):
            logger.info(f"key:{datan}")
            logger.info(f"ACTUAL_VALUE:[{res}]")
            logger.info(f"EXPECT_VALUE:[{expect_value}]")
            try:
                if isinstance(res, list):
                    assert expect_value in res
                else:
                    assert expect_value == res
            except AssertionError as e:
                self.return_value('FAIL')
                logger.info('--Fail--用例失败--')
                logger.exception(e)
                # raise
                str_result = 'FAIL'
            else:
                self.return_value('PASS')
                logger.info('--Pass--用例成功--')
                str_result = 'PASS'
        self.__allurestep(str_result)
        write_to_excel3(sheet, str_result, row_pos, col_pos_c)
        write_to_excel3(sheet, res, row_pos, col_pos_v)
        return str_result

    # def assertInText(self, data, sheet, row_pos, col_pos_c, col_pos_v):
    #     logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
    #     # dataL = str(data['input']).split(',')
    #     # d1 = str(dataL[0]).strip()
    #     # d2 = str(dataL[1]).strip()
    #     expect_value = str(data['request_data']).strip()
    #     d_k = str(data['input']).strip()
    #     pattern = f'"{d_k}": "{expect_value}"'
    #
    #     # if len(dataL) > 2:
    #     #     print('------------------Input data was wrong. Please check it.')
    #     result_to_json = json.dumps(self.jsonres)
    #     with allure.step(
    #             f"[{mTime()}]['assertInText'][key:{d_k},actual_value:{result_to_json}][expect_value:{expect_value}]"):
    #         logger.info(f"key:{d_k}")
    #         logger.info(f"ACTUAL_VALUE:[{result_to_json}]")
    #         logger.info(f"EXPECT_VALUE:[{pattern}]")
    #
    #         try:
    #             # json - --- dict json.loads(json_string) 接收的是一个json 字符串
    #             # dict - ---- json json.dumps(dict)接收的是一个字典 dict
    #             # print(result_to_json)  # 先转json
    #             # 方法2 直接判断包含
    #             assert pattern in result_to_json
    #         except AssertionError as e:
    #             self.return_value('FAIL')
    #             logger.info('--Fail--用例失败--')
    #             logger.exception(e)
    #             # raise
    #             str_result = 'FAIL'
    #             # return str_fail
    #         else:
    #             self.return_value('PASS')
    #             logger.info('--Pass--用例成功--')
    #             str_result = 'PASS'
    #     self.__allurestep(str_result)
    #     write_to_excel3(sheet, str_result, row_pos, col_pos_c)
    #     write_to_excel3(sheet, self.jsonres, row_pos, col_pos_v)
    #     return str_result

    def assertInRe(self, data, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
        expect_value = str(data['request_data']).strip()
        d_k = str(data['input']).strip()
        pattern = f'"{d_k}": "(.+?)"'

        # json - --- dict json.loads(json_string) 接收的是一个json 字符串
        # dict - ---- json json.dumps(dict)接收的是一个字典 dict
        # 断言data中包含"name": "yoyo"
        result_to_json = json.dumps(self.jsonres)
        # print(result_to_json)  # 先转json
        # 方法1 正则取值
        res = re.findall(pattern, result_to_json)  # 正则从json中取值
        with allure.step(
                f"[{mTime()}]['assertInRe'][key:{d_k},actual_value:{res}][expect_value:{expect_value}]"):
            logger.info(f"key:{d_k}")
            logger.info(f"ACTUAL_VALUE:[{res}]")
            logger.info(f"EXPECT_VALUE:[{expect_value}]")
            try:
                assert expect_value in res
                # 方法2 直接判断包含
                # assert '"name": "yoyo"' in result_to_json
            except AssertionError as e:
                self.return_value('FAIL')
                logger.info('--Fail--用例失败--')
                logger.exception(e)
                # raise
                str_result = 'FAIL'
            else:
                self.return_value('PASS')
                logger.info('--Pass--用例成功--')
                str_result = 'PASS'
        self.__allurestep(str_result)
        write_to_excel3(sheet, str_result, row_pos, col_pos_c)
        write_to_excel3(sheet, res, row_pos, col_pos_v)
        return str_result

    # def assertequals(self, data, sheet, row_pos, col_pos_c, col_pos_v):
    #     logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
    #     key = str(data['input']).strip()
    #     expect_value = str(data['request_data']).strip()
    #     actual_value = ''
    #     try:
    #         actual_value = str(self.jsonres[key])
    #     except:
    #         logger.error(f"{self.jsonres[key]} is not exist.")
    #         pass
    #     with allure.step(f"[{mTime()}]['assertequals'][key:{data['input']},actual_value:{actual_value}][expect_value:{expect_value}]"):
    #         logger.info(f"input key:[{data['input']}]")
    #         logger.info(f"ACTUAL_VALUE:[{actual_value}]")
    #         logger.info(f"EXPECT_VALUE:[{expect_value}]")
    #
    #         try:
    #             assert actual_value == expect_value
    #         except AssertionError as e:
    #             self.return_value('FAIL')
    #             logger.info('--Fail--用例失败--')
    #             logger.exception(e)
    #             # raise
    #             str_result = 'FAIL'
    #             # return str_fail
    #         else:
    #             self.return_value('PASS')
    #             logger.info('--成功--')
    #             str_result = 'PASS'
    #     self.__allurestep(str_result)
    #     write_to_excel3(sheet, str_result, row_pos, col_pos_c)
    #     write_to_excel3(sheet, str_result, row_pos, col_pos_v)
    #     return str_result
    def assertequals(self, data, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
        dictabspath = self.__abs(data['input'])
        expect_value = str(data['request_data']).strip()
        try:
            dict_value = eval(str(self.jsonres) + dictabspath)
            actual_value = str(dict_value)
        except Exception as e:
            logger.error(f"{str(self.jsonres) + dictabspath} is not exist.")
            logger.error(e)
            pass
        with allure.step(
                f"[{mTime()}]['assertequals'][key:{data['input']},actual_value:{actual_value}][expect_value:{expect_value}]"):
            logger.info(f"key:[{data['input']}]")
            logger.info(f"ACTUAL_VALUE:[{actual_value}]")
            logger.info(f"EXPECT_VALUE:[{expect_value}]")

            try:
                assert actual_value == expect_value
            except AssertionError as e:
                self.return_value('FAIL')
                logger.info('--Fail--用例失败--')
                logger.exception(e)
                # raise
                str_result = 'FAIL'
                # return str_fail
            else:
                self.return_value('PASS')
                logger.info('--Pass--用例成功--')
                str_result = 'PASS'
        self.__allurestep(str_result)
        write_to_excel3(sheet, str_result, row_pos, col_pos_c)
        write_to_excel3(sheet, actual_value, row_pos, col_pos_v)
        return str_result



    def savejson(self, data, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")

        with allure.step(f"[{mTime()}]['savejson'][relations_key:{data['input']}][jsonres_key:{data['request_data']}]"):
            logger.info(f"relations_key:[{data['input']}]")
            logger.info(f"jsonres_key:[{data['request_data']}]")
            logger.info(f"self.relations[{data['input']}] = self.jsonres[{data['request_data']}]")
            self.relations[data['input']] = self.jsonres[data['request_data']]
            self.return_value(self.relations[data['input']])
            write_to_excel3(sheet, 'PASS', row_pos, col_pos_c)
            write_to_excel3(sheet, self.jsonres[data['request_data']], row_pos, col_pos_v)
            return {f'{data["input"]}': f'{self.jsonres[data["request_data"]]}'}

    def addheader(self, data, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
        with allure.step(f"[{mTime()}]['addheader'][headers_key:{data['input']}][{data['request_data']}]"):
            logger.info(f"headers_key:[{data['input']}]")
            logger.info(f"headers_value_before:[{data['request_data']}]")
            logger.info(f"headers_value_after(__get_relations)[{self.__get_relations(data['request_data'])}]")
            # if data['input'] == 'token':
            self.session.headers[data['input']] = self.__get_relations(data['request_data'])
            # else:
            #     self.__hander_henders(data['input'])
            # self.return_value(self.__get_relations(data['request_data']))
            write_to_excel3(sheet, 'PASS', row_pos, col_pos_c)
            write_to_excel3(sheet, self.__get_relations(data['request_data']), row_pos, col_pos_v)
            return self.session.headers

    def seturl(self, data, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
        with allure.step(f"[{mTime()}]['seturl'][{data['input']}]"):
            path = str(data['input']).strip()
            if path.startswith('http'):
                self.url = data['input']
                self.return_value(self.url)
                write_to_excel3(sheet, 'PASS', row_pos, col_pos_c)
                write_to_excel3(sheet, data['input'], row_pos, col_pos_v)
            else:
                write_to_excel3(sheet, 'FAIL', row_pos, col_pos_c)
                write_to_excel3(sheet, data['input'], row_pos, col_pos_v)
            logger.info(f"输入参数:[{data['input']}]")


    def return_value(self, value):
        with allure.step(f"值是：{value}"):
            logger.info(f"值是：{value}")


    def post(self, data, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:【'post'】")

        #转为字典
        path = str(data['input']).strip()
        param = str(data['request_data']).strip()
        param = self.__get_data(param)
        # logger.info(f"input:[{data['input']}]")
        # logger.info(f"request_data:[{data['request_data']}]")

        new_url = ''
        if path.startswith('http'):
            pass
        else:
            if str(self.url)[-1:] == '/':
                new_url = self.url + path
            else:
                new_url = self.url + '/' + path
        with allure.step(fr"[{mTime()}][POST][post_after:{self.result}]"):
            try:
                self.return_value(f'请求接口:[{new_url}]')
                self.return_value(f'请求头:[{self.session.headers}]')
                self.return_value(f'请求参数:[{param}]')
                self.result = self.session.post(new_url, json=param, proxies=None)
                self.jsonres = json.loads(self.result.text)
                write_to_excel3(sheet, 'PASS', row_pos, col_pos_c)
                write_to_excel3(sheet, self.result.text, row_pos, col_pos_v)
            except Exception as e:
                # logger.error(f"It's not json text.\n{self.result.text}")
                logger.error(e)
                self.jsonres = self.result.text
                write_to_excel3(sheet, 'FAIL', row_pos, col_pos_c)
                write_to_excel3(sheet, self.result.text, row_pos, col_pos_v)
            self.return_value(f'返回值:[{self.jsonres}]')

        return self.jsonres




if __name__ == '__main__':
    pass
    # Http().seturl('aaaa')
    Http('11').assertequalsAbs('0123,aa,xx', 'sheet', 'row_pos', 'col_pos_c', 'col_pos_v')
    # a = getattr(Http, 'seturl')
    # print(a)
    # url = 'http://api.lemonban.com/futureloan/'
    # obj = Http()
    # a = getattr(obj, 'seturl')
    # print(a(url))
    # b = getattr(obj, 'post')
    # print(b)
    # print(b('member/register', '{"mobile_phone": "13800000618", "pwd": "1", "type": "1", "reg_name": "小可爱"}'))




    apidata2 = [{'case2': [{'num': '1', 'exec': 'y'}]}, {'case3': [{'num': '2', 'exec': 'y'}]}]

    d = apidata2[0].keys()
    print(d)
    print(list(d)[0])
