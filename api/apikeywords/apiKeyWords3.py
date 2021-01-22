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
        self.param = {}


        self.h1 = {"X-Lemonban-Media-Type": "lemonban.v2"}
        self.h2 = {"Content-Type": "application/json"}

    def __hander_henders(token=None):
        headers = {"X-Lemonban-Media-Type": "lemonban.v2",
                   "Content-Type": "application/json"}
        if token:
            headers["Authorization"] = "Bearer {}".format(token)
        return headers



    def __get_relations(self, param):
        pattern = r'[$][{][.*?][}]'
        if param is None or param == '':
            return None
        else:
            for key in self.relations:
                res = re.findall(pattern, param)
                if res:
                    for r in res:
                        param = param.replace('${' + key + '}', str(self.relations[key]))
                        logger.info(f"----------数据预处理after:--self.relations[key]>>{self.relations[key]}--")
            return param
    def __get_data(self, param):
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
            param = param.replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
            paramn = self.__get_relations(param)
            paramn = json.loads(paramn)
            logger.info(f"----------数据预处理before:--json.loads(paramn)>>{type(param)}>>{param}--")
            logger.info(f"----------数据预处理after :--json.loads(paramn)>>{type(paramn)}>>{paramn}--")
            return  paramn

    def __allurestep(self, str_fail='FAIL'):
        if str_fail == 'FAIL':
            with allure.step(f"对比结果：{str_fail}"):
                pass



    def assertJsonpath(self, apidata, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
        expect_value = str(apidata['request_data']).strip()
        datan = str(apidata['input']).strip()
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
        write_to_excel3(sheet, str(res), row_pos, col_pos_v)
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

    def assertInRe(self, apidata, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
        expect_value = str(apidata['request_data']).strip()
        d_k = str(apidata['input']).strip()
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
        write_to_excel3(sheet, str(res), row_pos, col_pos_v)
        return str_result

    def assertequals(self, apidata, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
        dictabspath = self.__abs(apidata['input'])
        expect_value = str(apidata['request_data']).strip()
        actual_value = ''
        try:
            dict_value = eval(str(self.jsonres) + dictabspath)
            actual_value = str(dict_value)
        except Exception as e:
            logger.error(f"{str(self.jsonres) + dictabspath} is not exist.")
            logger.error(e)
            pass
        with allure.step(
                f"[{mTime()}]['assertequals'][key:{apidata['input']},actual_value:{actual_value}][expect_value:{expect_value}]"):
            logger.info(f"key:[{apidata['input']}]")
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
        write_to_excel3(sheet, str(actual_value), row_pos, col_pos_v)
        return str_result

    def __abs(self, datan):
        dataL = datan.split(',')
        tmp = ''
        for one in dataL:
            if one.strip().isdigit():
                tmp = tmp + f"[{one.strip()}]"
            else:
                tmp = tmp + f"['{one.strip()}']"
        logger.info(f"----------数据预处理after:--__abs(datan)>>{datan}>>{tmp}--")
        return tmp

    def __get_re(self, param):
        pattern = r'[$][{](.*?)[}]'
        res = re.findall(pattern, str(param)) # ${aa}
        paramn = ''
        if res:
            for r in res:
                paramn = param.replace('${' + r + '}', r)
            logger.info(f"----------数据预处理after:--__get_re(param)>>{param}>>{paramn}--")
        return paramn

    def saveparam(self, apidata, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")

        try:
            input_path = apidata['input'].strip()
            _data = apidata['request_data'].strip()
            if str(_data).startswith('{') and str(_data).endswith('}'):
                request_data_value = self.__get_data(_data)
            else:
                request_data_value = self.__get_relations(_data) # ???
                # request_data_path = self.__abs(_data)
                # request_data_value = eval(str(self.jsonres) + request_data_path)
            with allure.step(f"[{mTime()}]['saveparam'][saveparam_key:{input_path}][saveparam_value:{request_data_value}]"):
                logger.info(f"saveparam_key:[{input_path}]")
                logger.info(f"saveparam_value:[{request_data_value}]")
                logger.info(f"self.param[{input_path}] = {request_data_value}")

                self.param[input_path] = request_data_value
                self.return_value(self.param)
                write_to_excel3(sheet, 'PASS', row_pos, col_pos_c)
                write_to_excel3(sheet, str(request_data_value), row_pos, col_pos_v) # self.jsonres[data['request_data']]
                return {f'{input_path}': f'{request_data_value}'}

        except Exception as e:
            write_to_excel3(sheet, 'FAIL', row_pos, col_pos_c)
            logger.error(e)
            pass

    def savedata(self, apidata, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")

        request_data_path = apidata['request_data'].strip()
        try:
            with allure.step(
                    f"[{mTime()}]['savedata'][relations_key:{apidata['input']}][relations_value:{request_data_path}]"):
                logger.info(f"relations_key:[{apidata['input']}]")
                logger.info(f"relations_value:[{request_data_path}]")
                logger.info(f"self.relations[{apidata['input']}] = {request_data_path}")
                if str(request_data_path).startswith('${'):
                    write_to_excel3(sheet, 'FAIL', row_pos, col_pos_c)
                    write_to_excel3(sheet, str(request_data_path), row_pos, col_pos_v)
                else:
                    self.relations[apidata['input'].strip()] = request_data_path
                    self.return_value(self.relations[apidata['input'].strip()])
                    write_to_excel3(sheet, 'PASS', row_pos, col_pos_c)
                    write_to_excel3(sheet, str(request_data_path), row_pos, col_pos_v) # self.jsonres[data['request_data']]
                return {f'{apidata["input"].strip()}': f'{request_data_path}'}
        except Exception as e:
            write_to_excel3(sheet, 'FAIL', row_pos, col_pos_c)
            logger.error(e)

    def savejson(self, apidata, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")

        try:
            request_data_path = self.__abs(apidata['request_data'].strip())
            request_data_value = eval(str(self.jsonres) + request_data_path)

            with allure.step(f"[{mTime()}]['savejson'][relations_key:{apidata['input']}][jsonres_key:{request_data_path}]"):
                logger.info(f"relations_key:[{apidata['input']}]")
                logger.info(f"jsonres_key:[{request_data_path}]")
                logger.info(f"self.relations[{apidata['input']}] = self.jsonres{request_data_path}")

                self.relations[apidata['input'].strip()] = str(request_data_value)
                self.return_value(self.relations[apidata['input'].strip()])
                write_to_excel3(sheet, 'PASS', row_pos, col_pos_c)
                write_to_excel3(sheet, str(request_data_value), row_pos, col_pos_v) # self.jsonres[data['request_data']]
                return {f'{apidata["input"].strip()}': f'{request_data_value}'}

        except Exception as e:
            write_to_excel3(sheet, 'FAIL', row_pos, col_pos_c)
            return_str = f"key:'{request_data_path}'is not in {str(self.jsonres)}."
            write_to_excel3(sheet, str(return_str), row_pos, col_pos_v)
            logger.error(return_str)
            logger.error(e)
            pass

    def addheader(self, apidata, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
        try:
            with allure.step(f"[{mTime()}]['addheader'][headers_key:{apidata['input']}][{apidata['request_data']}]"):
                logger.info(f"headers_key:[{apidata['input']}]")
                logger.info(f"headers_value_before:[{apidata['request_data']}]")
                rel = self.__get_relations(apidata['request_data'].strip())
                logger.info(f"headers_value_after(__get_relations):[{rel}]")

                self.session.headers[apidata['input'].strip()] = rel
                # self.return_value(rel)
                write_to_excel3(sheet, 'PASS', row_pos, col_pos_c)
                write_to_excel3(sheet, str(rel), row_pos, col_pos_v)
                return self.session.headers
        except Exception as e:
            logger.error(f"key:'{self.__get_re(apidata['request_data'].strip())}' is not in [{self.relations}].")
            logger.error(e)
            pass

    def seturl(self, apidata, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:{sys._getframe().f_code.co_name}")
        try:
            with allure.step(f"[{mTime()}]['seturl'][{apidata['input']}]"):
                logger.info(f"输入参数:[{apidata['input']}]")
                path = str(apidata['input']).strip()
                if path.startswith('http'):
                    self.url = path
                    self.return_value(self.url)
                    write_to_excel3(sheet, 'PASS', row_pos, col_pos_c)
                    write_to_excel3(sheet, str(apidata['input']), row_pos, col_pos_v)
                else:
                    write_to_excel3(sheet, 'FAIL', row_pos, col_pos_c)
                    write_to_excel3(sheet, str(apidata['input']), row_pos, col_pos_v)
        except Exception as e:
            logger.error(f"Execute method '{sys._getframe().f_code.co_name}' error.")
            logger.error(e)
            pass


    def return_value(self, value):
        with allure.step(f"值是：{value}"):
            logger.info(f"值是：{value}")


    def post(self, apidata, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:【'post'】")

        new_url = ''
        url_path = str(apidata['input']).strip()
        _data = apidata['request_data'].strip()
        if url_path.startswith('http'):
            new_url = url_path
        else:
            if str(self.url)[-1:] == '/':
                new_url = self.url + url_path
            else:
                new_url = self.url + '/' + url_path
        # 转为字典
        try:
            with allure.step(fr"[{mTime()}]['POST'][post_after:{self.result}]"):
                new_url = self.__get_relations(new_url)
                self.return_value(f'请求接口:[{new_url}]')
                self.return_value(f'请求头:[{self.session.headers}]')
                _data = self.__get_data(_data)

                self.return_value(f'请求体:[{_data}]')
                self.result = self.session.post(new_url, json=_data, data=None, proxies=None)
                self.jsonres = json.loads(self.result.text)
                self.return_value(f'返回值:[{json.loads(self.result.text)}]')
                write_to_excel3(sheet, 'PASS', row_pos, col_pos_c)
                write_to_excel3(sheet, str(self.jsonres), row_pos, col_pos_v)
        except Exception as e:
            logger.error(f"Execute method '{sys._getframe().f_code.co_name}' error.")
            logger.error(e)
            write_to_excel3(sheet, 'FAIL', row_pos, col_pos_c)
            write_to_excel3(sheet, str(self.result.text), row_pos, col_pos_v)
        finally:
            self.param = {}
        return self.jsonres

    def get(self, apidata, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:【'get'】")

        new_url = ''
        url_path = str(apidata['input']).strip()
        if url_path.startswith('http'):
            new_url = url_path
        else:
            if str(self.url)[-1:] == '/':
                new_url = self.url + url_path
            else:
                new_url = self.url + '/' + url_path
        # 转为字典
        try:
            with allure.step(fr"[{mTime()}]['POST'][post_after:{self.result}]"):
                new_url = self.__get_relations(new_url)
                self.return_value(f'请求接口:[{new_url}]')
                self.return_value(f'请求头:[{self.session.headers}]')
                _data = self.param

                self.return_value(f'请求体:[{_data}]')
                self.result = self.session.post(new_url, params=_data, proxies=None)
                self.jsonres = json.loads(self.result.text)
                self.return_value(f'返回值:[{json.loads(self.result.text)}]')
                write_to_excel3(sheet, 'PASS', row_pos, col_pos_c)
                write_to_excel3(sheet, str(self.jsonres), row_pos, col_pos_v)
        except Exception as e:
            logger.error(f"Execute method '{sys._getframe().f_code.co_name}' error.")
            logger.error(e)
            write_to_excel3(sheet, 'FAIL', row_pos, col_pos_c)
            write_to_excel3(sheet, str(self.result.text), row_pos, col_pos_v)
        finally:
            self.param = {}
        return self.jsonres
    def py_get(self, apidata, sheet, row_pos, col_pos_c, col_pos_v):
        logger.info(f"执行函数:【'get'】")

        url_path = str(apidata['input']).strip()
        _data = apidata['request_data'].strip()
        if url_path.startswith('http'):
            new_url = url_path
        else:
            if str(self.url)[-1:] == '/':
                new_url = self.url + url_path
            else:
                new_url = self.url + '/' + url_path
        # 转为字典
        try:
            with allure.step(fr"[{mTime()}]['POST'][post_after:{self.result}]"):
                new_url = self.__get_relations(new_url)
                self.return_value(f'请求接口:[{new_url}]')
                self.return_value(f'请求头:[{self.session.headers}]')
                _data = self.param

                self.return_value(f'请求体:[{_data}]')
                self.result = self.session.post(new_url, params=_data, proxies=None)
                self.jsonres = json.loads(self.result.text)
                self.return_value(f'返回值:[{json.loads(self.result.text)}]')
                write_to_excel3(sheet, 'PASS', row_pos, col_pos_c)
                write_to_excel3(sheet, str(self.jsonres), row_pos, col_pos_v)
        except Exception as e:
            logger.error(f"Execute method '{sys._getframe().f_code.co_name}' error.")
            logger.error(e)
            write_to_excel3(sheet, 'FAIL', row_pos, col_pos_c)
            write_to_excel3(sheet, str(self.result.text), row_pos, col_pos_v)
        finally:
            self.param = {}
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
