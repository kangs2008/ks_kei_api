from configparser import ConfigParser


class HandleConfig:
    '''
    定义一个配置文件处理类
    '''
    def __init__(self, filename):
        self.filename = filename  # 配置文件名
        self.config = ConfigParser()  # 创建一个配置文件对象
        self.config.read(self.filename, encoding='utf-8')  # 调用配置文件对象的读取方法，并传入一个配置文件名

    def get_value(self, section, option):  # 获取字符串类型的选项值
        return self.config.get(section, option)

    def get_int(self, section, option):  # 获取整型的选项值
        return self.config.getint(section, option)

    def get_float(self, section, option):  # 获取浮点型的选项值
        return self.config.getfloat(section, option)

    def get_boolean(self, section, option):  # 获取布尔类型的选项值
        return self.config.getboolean(section, option)

    def get_eval_data(self, section, option):  # 获取python内置类型的选项值
        return eval(self.config.get(section, option))

    @staticmethod
    def write_value(filename, data):  # 写入配置信息
        '''
        定义一个写入配置文件的方法
        :param filename: 配置文件名，建议重新命名
        :param data: 嵌套字典的字典，键为区域名，嵌套的区域值为选项名和选项值的字典
        :return:
        '''
        config = ConfigParser()
        if isinstance(data, dict):
            for key in data:  # 遍历一个嵌套字典的字典，并将取得的值赋给配置文件对象的选项名和选项值
                config[key] = data[key]  #
                # 创建一个配置文件并将获取到的配置信息使用配置文件对象的写入方法进行写入
            with open(filename, mode='w', encoding='utf-8') as f:
                config.write(f)