import pytest

def pytest_addoption(parser):
    parser.addoption("--file", default=r'D:\desk20201127\ks\Datas', help='指定文件名字 or 文件夹')
    parser.addoption("--sheet", default=None, help='None 指定文件 sheet name, 默认遍历文件里所有 sheet name')
    parser.addoption("--folder", default=None,  help='None 输入任意字符，表示遍历文件和文件夹，默认只读取当前文件夹的文件(文件夹不读取)')

@pytest.fixture
def file(pytestconfig):
    return pytestconfig.getoption("--file")

@pytest.fixture
def sheet(pytestconfig):
    return pytestconfig.getoption("--sheet")

@pytest.fixture
def folder(pytestconfig):
    return pytestconfig.getoption("--folder")
