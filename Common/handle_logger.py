import logging, os
import logging.handlers
from Common.setting import REPORT_DIR, LOG_DIR, REPORT_CURRENT_DIR
from Common.handle_config import ReadWriteConfFile

get_logdir = ReadWriteConfFile().get_option('report_dir', 'report_dir_folder')
num = ReadWriteConfFile().get_option('report_file', 'file_num')
log_dir = os.path.join(REPORT_DIR, get_logdir)
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
log_file_format = os.path.join(log_dir, f'{get_logdir}_{num}.log')

log_file = os.path.join(LOG_DIR, 'Test.log')

class HandleLogger:
    """
    定义一个日志处理类
    """
    def __init__(self):
        self.case_logger = logging.getLogger('LOG')  # 创建一个日志收集器
        fmt = '%(asctime)s %(name)s %(levelname)s %(filename)s-%(lineno)d line：%(message)s'
        self.case_logger.setLevel(logging.DEBUG)  # 指定日志收集器的日志等级

        sizefilehandler = logging.handlers.RotatingFileHandler(log_file, mode='a', maxBytes=1024*1024*5, backupCount=10,
                                                               encoding='utf-8', delay=False)
        console_handle = logging.StreamHandler()  # 定义一个控制台输出渠道
        file_handle2 = logging.FileHandler(log_file, encoding='utf-8')  # 定义一个文件输出渠道
        file_handle = logging.FileHandler(log_file_format, encoding='utf-8')

        console_handle.setLevel(logging.ERROR)  # 设置控制台输出渠道的日志级别为ERROR
        file_handle.setLevel(logging.INFO)  # 设置文件输出渠道的日志级别为INFO
        file_handle2.setLevel(logging.INFO)

        simple_formatter = logging.Formatter(fmt)  # 定义简洁类型日志格式
        verbose_formatter = logging.Formatter(fmt)  # 定义详细类型日志格式

        console_handle.setFormatter(simple_formatter)  # 控制台显示简洁的日志
        file_handle.setFormatter(verbose_formatter)  # 文件中显示详细的日志
        file_handle2.setFormatter(verbose_formatter)

        # 将日志收集器与输出渠道对接
        self.case_logger.addHandler(sizefilehandler)
        self.case_logger.addHandler(console_handle)
        self.case_logger.addHandler(file_handle)
        self.case_logger.addHandler(file_handle2)

    def get_case_logger(self):  # 获取日志收集器
        return self.case_logger

do_case = HandleLogger()  # 创建一个日志对象
logger = do_case.get_case_logger()  # 创建一个日志器方法