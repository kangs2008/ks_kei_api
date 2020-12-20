from configparser import ConfigParser
import os
# from demo import settings  # django项目的配置文件
from Common.setting import BASE_DIR

class ReadWriteConfFile(object):
    # path = settings.BASE_DIR + os.sep + 'config.ini'  # 可根据需要替换成自己的路径
    path = os.path.join(BASE_DIR, 'exec_file.ini')
    print('path::::', path)
    # @staticmethod
    def get_parser(self):
        cf = ConfigParser()
        cf.read(ReadWriteConfFile().path, encoding='utf-8')
        return cf

    # @staticmethod
    def write_parser(self, cf):
        f = open(ReadWriteConfFile().path, "w", encoding='utf-8')
        cf.write(f)
        f.close()

    # @staticmethod
    def add_section(self, section):
        cf = ReadWriteConfFile().get_parser()
        all_sections = cf.sections()
        if section in all_sections:
            return
        else:
            cf.add_section(section)
            ReadWriteConfFile().write_parser(cf)

    # @staticmethod
    def get_option(self, section, key):
        cf = ReadWriteConfFile().get_parser()
        return cf.get(section, key)

    # @staticmethod
    def set_option(self, section, key, value):
        cf = ReadWriteConfFile().get_parser()
        cf.set(section, key, value)
        ReadWriteConfFile().write_parser(cf)


if __name__ == '__main__':
    # ReadWriteConfFile.add_section('exec')
    ReadWriteConfFile().set_option('exec', 'exec_file_path', 'sophia2')
    x = ReadWriteConfFile().get_option('exec', 'exec_file_path')
    print(x)