import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HandleRequests:

    def __init__(self):
        self.one_session = requests.Session()

    def request(self, url, method='get', headers=None, param=None, data=None, is_json=False, is_http=False):
        '''
        定义一个请求方法
        :param url: 域名接口
        :param method: 请求方法
        :param headers: 请求头
        :param param: get请求体
        :param data: post表单请求体
        :param is_json: 是否为json请求数据
        :param is_http: 是否为http请求
        :return: 请求结果
        '''
        if is_http is False:
            if method.lower() == 'get':
                res = self.one_session.get(url=url, headers=headers, params=param, verify=False)
                return res
            elif method.lower() == 'post':
                if is_json:
                    res = self.one_session.post(url=url, headers=headers, data=data, verify=False)
                    return res
                else:
                    res = self.one_session.post(url=url, headers=headers, json=data, verify=False)
                    return res
            elif method.lower() == 'delete':
                res = self.one_session.delete(url=url, headers=headers, verify=False)
                return res
            else:
                print("不支持{}请求方法！".format(method))
        else:
            if method.lower() == 'get':
                res = self.one_session.get(url=url, headers=headers, params=data)
                return res
            elif method.lower() == 'post':
                if is_json:
                    res = self.one_session.post(url=url, headers=headers, data=data)
                    return res
                else:
                    res = self.one_session.post(url=url, headers=headers, json=data)
                    return res
            elif method.lower() == 'delete':
                res = self.one_session.delete(url=url, headers=headers)
                return res
            else:
                print("不支持{}请求方法！".format(method))

    def close_cookie(self):
        '''
        关闭cookie
        '''
        self.one_session.close()