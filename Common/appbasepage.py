import time
from datetime import datetime
import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.webdriver import WebDriver
from Common.handle_logger import case_logger
from Common.setting import OUTPUTS_DIR


class BasePage:
    '''
    BasePage类，针对PageObjects类的二次封装
    '''

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def wait_element_to_be_visible(self, loc, img_doc, timeout=20, frequency=0.5):
        '''
        等待元素可见
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        '''
        try:
            case_logger.info("开始等待页面元素<{}>是否可见！".format(loc))
            start_time = time.time()
            WebDriverWait(self.driver, timeout, frequency).until(EC.visibility_of_element_located(loc))
        except Exception as e:
            case_logger.error("页面元素<{}>等待可见失败！".format(loc))
            self.save_screenshot(img_doc)
            raise e
        else:
            end_time = time.time()
            case_logger.info("页面元素<{}>等待可见，等待时间：{}秒".format(loc, round(end_time - start_time, 2)))

    def wait_element_to_be_click(self, loc, img_doc, timeout=20, frequency=0.5):
        '''
        等待元素可点击
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        '''
        try:
            case_logger.info("开始等待页面元素<{}>是否可点击！".format(loc))
            start_time = time.time()
            WebDriverWait(self.driver, timeout, frequency).until(EC.element_to_be_clickable(loc))
        except Exception as e:
            case_logger.error("页面元素<{}>等待可点击失败！".format(loc))
            self.save_screenshot(img_doc)
            raise e
        else:
            end_time = time.time()
            case_logger.info("页面元素<{}>等待可点击，等待时间：{}秒".format(loc, round(end_time - start_time, 2)))

    def wait_element_to_be_exist(self, loc, img_doc, timeout=20, frequency=0.5):
        '''
        等待元素存在
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        '''
        try:
            case_logger.info("开始等待页面元素<{}>是否存在！".format(loc))
            start_time = time.time()
            WebDriverWait(self.driver, timeout, frequency).until(EC.presence_of_element_located(loc))
        except Exception as e:
            case_logger.error("页面元素<{}>等待存在失败！".format(loc))
            self.save_screenshot(img_doc)
            raise e
        else:
            end_time = time.time()
            case_logger.info("页面元素<{}>等待存在，等待时间：{}秒".format(loc, round(end_time - start_time, 2)))

    def save_screenshot(self, img_doc):
        '''
        页面截屏保存截图
        :param img_doc: 截图说明
        :return:
        '''
        file_name = OUTPUTS_DIR + "\\{}_{}.png".format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"), img_doc)
        self.driver.save_screenshot(file_name)
        with open(file_name, mode='rb') as f:
            file = f.read()
        allure.attach(file, img_doc, allure.attachment_type.PNG)
        case_logger.info("页面截图文件保存在：{}".format(file_name))

    def get_element(self, loc, img_doc):
        '''
        获取页面中的元素
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :return: WebElement对象
        '''
        case_logger.info("在{}中查找元素<{}>".format(img_doc, loc))
        try:
            ele = self.driver.find_element(*loc)
        except Exception as e:
            case_logger.error("在{}中查找元素<{}>失败！".format(img_doc, loc))
            self.save_screenshot(img_doc)
            raise e
        else:
            return ele

    def get_elements(self, loc, img_doc):
        '''
        获取页面中的所有元素
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :return: WebElement对象
        '''
        case_logger.info("在{}中查找所有元素<{}>".format(img_doc, loc))
        try:
            ele = self.driver.find_elements(*loc)
        except Exception as e:
            case_logger.error("在{}中查找所有元素<{}>失败！".format(img_doc, loc))
            self.save_screenshot(img_doc)
            raise e
        else:
            return ele

    def input_text(self, text, loc, img_doc, timeout=20, frequency=0.5):
        '''
        对输入框输入文本内容
        :param text: 输入的文本内容
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        '''
        try:
            case_logger.info("在{}中输入元素<{}>的内容为{}".format(img_doc, loc, text))
            self.wait_element_to_be_visible(loc, img_doc, timeout, frequency)
            self.get_element(loc, img_doc).send_keys(text)
        except Exception as e:
            case_logger.error("在元素<{}>中输入内容{}失败！".format(loc, text))
            self.save_screenshot(img_doc)
            raise e

    def clear_text(self, loc, img_doc, timeout=20, frequency=0.5):
        '''
        清除文本框的内容
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        '''
        try:
            case_logger.info("在{}中清除元素<{}>的文本内容".format(img_doc, loc))
            self.wait_element_to_be_click(loc, img_doc, timeout, frequency)
            self.get_element(loc, img_doc).clear()
        except Exception as e:
            case_logger.error("在{}中清除元素<{}>的文本内容失败！".format(img_doc, loc))
            self.save_screenshot(img_doc)
            raise e

    def click_button(self, loc, img_doc, timeout=20, frequency=0.5):
        '''
        点击按钮
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        '''
        try:
            case_logger.info("在{}中点击元素<{}>".format(img_doc, loc))
            self.wait_element_to_be_click(loc, img_doc, timeout, frequency)
            self.get_element(loc, img_doc).click()
        except Exception as e:
            case_logger.error("在{}中点击元素<{}>失败！".format(img_doc, loc))
            self.save_screenshot(img_doc)
            raise e

    def get_element_text(self, loc, img_doc, timeout=20, frequency=0.5):
        '''
        获取WebElement对象的文本值
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return: WebElement对象的文本值
        '''
        try:
            case_logger.info("在{}中获取元素<{}>的文本值".format(img_doc, loc))
            self.wait_element_to_be_visible(loc, img_doc, timeout, frequency)
            text = self.get_element(loc, img_doc).text
        except Exception as e:
            case_logger.error("在{}中获取元素<{}>的文本值失败！".format(img_doc, loc))
            self.save_screenshot(img_doc)
            raise e
        else:
            case_logger.info("获取到的元素文本值为：{}".format(text))
            return text

    def get_elements_text(self, loc, img_doc, timeout=20, frequency=0.5):
        '''
        获取WebElement对象的所有文本值
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return: WebElement对象的文本值的列表
        '''
        try:
            case_logger.info("在{}中获取元素<{}>的所有文本值".format(img_doc, loc))
            self.wait_element_to_be_visible(loc, img_doc, timeout, frequency)
            all_text = self.get_elements(loc, img_doc)
            text_list = []
            for one_text in all_text:
                text_list.append(one_text.text)
        except Exception as e:
            case_logger.error("在{}中获取元素<{}>的所有文本值失败！".format(img_doc, loc))
            self.save_screenshot(img_doc)
            raise e
        else:
            case_logger.info("获取到的元素文本值列表为：{}".format(text_list))
            return text_list

    def get_element_attr(self, attr_name, loc, img_doc, timeout=20, frequency=0.5):
        '''
        获取WebElement对象的属性值
        :param attr_name: 属性名称
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return: WebElement对象的属性值
        '''
        try:
            case_logger.info("在{}中获取元素<{}>的属性{}的值".format(img_doc, loc, attr_name))
            self.wait_element_to_be_exist(loc, img_doc, timeout, frequency)
            value = self.get_element(loc, img_doc).get_attribute(attr_name)
        except Exception as e:
            case_logger.error("在{}中获取元素<{}>的属性{}的值失败！".format(img_doc, loc, attr_name))
            self.save_screenshot(img_doc)
            raise e
        else:
            case_logger.info("获取到的元素属性{}的值为{}".format(attr_name, value))
            return value

    def sliding_screen(self, direction, img_doc):
        '''
        滑屏操作
        :param direction: 滑屏方向：上-up；下-down；左-left；右-right
        :param img_doc: 截图说明
        :return:
        '''
        size = self.driver.get_window_size()
        try:
            case_logger.info("开始向{}方向滑动".format(direction))
            if direction.lower() == 'up':
                self.driver.swipe(start_x=size['width'] * 0.5,
                                  start_y=size['height'] * 0.9,
                                  end_x=size['width'] * 0.5,
                                  end_y=size['height'] * 0.1,
                                  duration=200)
            elif direction.lower() == 'down':
                self.driver.swipe(start_x=size['width'] * 0.5,
                                  start_y=size['height'] * 0.1,
                                  end_x=size['width'] * 0.5,
                                  end_y=size['height'] * 0.9,
                                  duration=200)
            elif direction.lower() == 'left':
                self.driver.swipe(start_x=size['width'] * 0.9,
                                  start_y=size['height'] * 0.5,
                                  end_x=size['width'] * 0.1,
                                  end_y=size['height'] * 0.5,
                                  duration=200)
            elif direction.lower() == 'right':
                self.driver.swipe(start_x=size['width'] * 0.1,
                                  start_y=size['height'] * 0.5,
                                  end_x=size['width'] * 0.9,
                                  end_y=size['height'] * 0.5,
                                  duration=200)
            else:
                case_logger.error("方向选择错误！")
        except Exception as e:
            case_logger.error("向{}方向滑动屏幕失败！".format(direction))
            self.save_screenshot(img_doc)
            raise e

    def get_toast_msg(self, partial_text, img_doc):
        '''
        获取toast文本信息
        :param partial_text: 不完整文本
        :param img_doc: 截图说明
        :return: toast文本
        '''
        loc = (MobileBy.XPATH, '//*[contains(@text,"{}")]'.format(partial_text))
        try:
            WebDriverWait(self.driver, 10, 0.01).until(EC.presence_of_element_located(loc))
            msg = self.driver.find_element(*loc).text
            print("toast出现了！！！")
            return msg
        except Exception as e:
            print("好可惜，toast没找到！！")
            case_logger.error("获取toast文本失败！")
            self.save_screenshot(img_doc)
            raise e

    def switch_to_webview(self, loc, img_doc, timeout=20, frequency=0.5):
        '''
        切换到webview页面
        :param loc: webview页面的元素
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        '''
        try:
            case_logger.info("等待元素{}可见，并进行webview切换".format(loc))
            start_time = time.time()
            WebDriverWait(self.driver, timeout, frequency).until(EC.visibility_of_element_located(loc))
            cons = self.driver.contexts
            case_logger.info("开始切换到webview：{}".format(cons[-1]))
            self.driver.switch_to.context(cons[-1])
        except Exception as e:
            case_logger.error("切换webview失败！")
            self.save_screenshot(img_doc)
            raise e
        else:
            end_time = time.time()
            case_logger.info("切换到webview：{}成功，等待时间：{}秒".format(cons[-1], round(end_time - start_time, 2)))

    def switch_to_native_app(self, img_doc):
        '''
        切换到app原生页面
        :param img_doc: 截图说明
        :return:
        '''
        try:
            case_logger.info("切换到app原生页面")
            self.driver.switch_to.context('NATIVE_APP')
        except Exception as e:
            case_logger.error("切换到app原生页面失败！")
            self.save_screenshot(img_doc)
            raise e

    def application_switching(self, package_name, activity_name, img_doc):
        '''
        应用切换
        :param package_name: 包名
        :param activity_name: 欢迎页面名
        :param img_doc: 截图说明
        :return:
        '''
        try:
            case_logger.info("切换应用到{}".format(package_name))
            self.driver.start_activity(app_package=package_name, app_activity=activity_name)
        except Exception as e:
            case_logger.error("切换应用到{}失败！".format(package_name))
            self.save_screenshot(img_doc)
            raise e