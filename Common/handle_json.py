import json


class HandleJson:
    '''
    定义一个json格式数据处理类
    '''

    @staticmethod
    def loads_data(data):
        '''
        将json数据格式的数据转换为字典型的数据类型
        :param data: json格式字符串
        :return: 字典数据类型
        '''
        dict_ison = json.loads(data)
        return dict_ison

    @staticmethod
    def load_data(filename):
        '''
        读取json文件中的json数据并转换为字典型的数据类型
        :param filename:json文件名
        :return:字典数据类型
        '''
        with open(filename, mode='r', encoding='utf-8') as fp:
            dict_file = json.load(fp)
        return dict_file

    @staticmethod
    def dumps_data(data):
        '''
        将字典数据类型转换为json格式类型数据
        :param data: 字典数据类型
        :return: json格式字符串
        '''
        json_dict = json.dumps(data, ensure_ascii=False)
        return json_dict

    @staticmethod
    def dump(data, filename):
        '''
        将字典数据类型转换为json格式数据并存储到json格式的文件中
        :param data: 字典数据类型
        :param filename: json文件名
        :return: json格式文件
        '''
        with open(filename, mode='w', encoding='utf-8') as fp:
            json.dump(data, fp)