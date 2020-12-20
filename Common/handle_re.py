import re
import os
from Common.handle_mysql import HandleMysql
from Common.handle_config import HandleConfig
from Common.setting import BASE_DIR


class HandleParam:
    '''
    定义一个参数化类
    '''

    not_exist_mobile = r'\${is_not_exist_mobile}'
    admin_user_mobile = r'\${admin_user_mobile}'
    user_id = r'\${user_id}'

    @classmethod
    def param_not_exist_phone_num(cls, data):
        '''
        参数化未注册手机号
        :param data: 参数化data
        :return:
        '''
        if re.search(r'\${\w+}', data) is not None:
            do_mysql = HandleMysql()
            data = re.sub(cls.not_exist_mobile, str(do_mysql.is_not_exist_mobile()), data)
            do_mysql.close()
            return data
        else:
            return data

    @classmethod
    def param_admin_user_phone_num(cls, data):
        '''
        参数化管理员手机号
        :param data: 参数化data
        :return:
        '''
        if re.search(r'\${\w+}', data) is not None:
            user_conf = HandleConfig(os.path.join(BASE_DIR, 'three_user_info.ini'))
            data = re.sub(cls.admin_user_mobile, str(user_conf.get_int("manage_user", "mobilephone")), data)
            return data
        else:
            return data

    @classmethod
    def param_user_id(cls, data):
        '''
        参数化用户id
        :param data: 参数化data
        :return:
        '''
        if re.search(r'\${\w+}', data) is not None:
            user_id = getattr(do_re, 'user_id')
            data = re.sub(cls.user_id, str(user_id), data)
            return data
        else:
            return data

    @classmethod
    def parametrization(cls, data):
        '''
        批量参数化方法
        :param data: 参数化data
        :return:
        '''
        data = cls.param_not_exist_phone_num(data)
        data = cls.param_exist_phone_num(data)
        data = cls.param_user_id(data)
        return data

do_re = HandleParam()  # 创建一个参数化对象