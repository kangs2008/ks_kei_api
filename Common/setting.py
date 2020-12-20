import os

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取Configs目录路径
#CONFIG_DIR = os.path.join(BASE_DIR, 'Configs')

# 获取配置文件路径
#CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, 'init.ini')

# 获取TestDatas目录路径
DATAS_DIR = os.path.join(BASE_DIR, 'Datas')

# 获取excel文件路径
DATAS_FILE_PATH = os.path.join(DATAS_DIR, 'TestDatas.xlsx')

# 获取Report目录路径
REPORT_DIR = os.path.join(BASE_DIR, 'Report')

# 获取Log目录路径
LOG_DIR = os.path.join(BASE_DIR, 'Logs')

# 获取Reports/PIC目录路径
PIC_DIR = os.path.join(REPORT_DIR, 'PIC')

# 获取TestCases目录路径
CASES_DIR = os.path.join(BASE_DIR, 'TestCases')