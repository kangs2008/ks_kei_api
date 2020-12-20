import time, os, sys
import datetime
import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from Common.handle_logger import logger as case_logger
from Common.setting import PIC_DIR
# from Common.upload_file import upload


class BasePage:
    """
    BasePage类
    """

    def __init__(self, driver):
        self.driver = driver

    def switch_to_frame(self, loc, img_doc, timeout=20, frequency=0.5):
        """
        切换iframe页面
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        """
        try:
            case_logger.info("<{}>在{}中根据元素<{}>进行iframe切换".format(sys._getframe().f_code.co_name, img_doc, loc))
            start_time = time.time()
            WebDriverWait(self.driver, timeout, frequency).until(EC.frame_to_be_available_and_switch_to_it(loc))
        except Exception as e:
            case_logger.error("<{}>在{}中根据元素<{}>进行iframe切换失败！".format(sys._getframe().f_code.co_name, img_doc, loc))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))
        else:
            end_time = time.time()
            case_logger.info("<{}>在{}中根据元素<{}>进行iframe切换，等待时间：{}秒".
                             format(sys._getframe().f_code.co_name, img_doc, loc, round(end_time - start_time, 2)))

    def switch_to_default_content(self, img_doc):
        """
        切换iframe到main页面
        :param img_doc: 截图说明
        :return:
        """
        try:
            case_logger.info(f"<{sys._getframe().f_code.co_name}>切换iframe到main页面")
            self.driver.switch_to.default_content()
        except Exception as e:
            case_logger.error(f"<{sys._getframe().f_code.co_name}>切换iframe到main页面失败！")
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))

    def switch_to_parent(self, img_doc):
        """
        切换iframe到上一层页面
        :param img_doc: 截图说明
        :return:
        """
        try:
            case_logger.info(f"<{sys._getframe().f_code.co_name}>切换iframe到上一层页面")
            self.driver.switch_to.parent_frame()
        except Exception as e:
            case_logger.error(f"<{sys._getframe().f_code.co_name}>切换iframe到上一层页面失败！")
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))

    # def upload_file(self, filename, img_doc, browser_type="chrome"):
    #     """
    #     非input标签的文件上传
    #     :param filename: 文件名（绝对路径）
    #     :param img_doc: 截图说明
    #     :param browser_type: 浏览器类型
    #     :return:
    #     """
    #     try:
    #         case_logger.info("上传文件（{}）".format(filename))
    #         time.sleep(2)
    #         upload(filePath=filename, browser_type=browser_type)
    #     except Exception as e:
    #         case_logger.error("上传文件（{}）失败！".format(filename))
    #         self.save_screenshot(img_doc)
    #         raise e
    #     else:
    #         time.sleep(2)

    def suspend_mouse(self, loc, img_doc, timeout=20, frequency=0.5):
        """
        鼠标悬浮
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        """
        try:
            case_logger.info("<{}>在{}上根据元素<{}>进行悬浮".format(sys._getframe().f_code.co_name, img_doc, loc))
            self.wait_ele_to_click(loc, img_doc, timeout, frequency)
            # ele = self.get_ele(loc, img_doc)
            ele = self.driver.find_element(*loc)
            ActionChains(self.driver).move_to_element(ele).perform()
        except Exception as e:
            case_logger.error("<{}>在{}上根据元素<{}>进行悬浮失败！".format(sys._getframe().f_code.co_name, img_doc, loc))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))

    def alert_close(self, img_doc, alert_type='alert', text=None, timeout=20, frequency=0.5):
        """
        弹框关闭
        :param img_doc: 截图说明
        :param alert_type: 弹框类型：alert/confirm/prompt
        :param text: prompt弹框输入的文本
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        """
        try:
            case_logger.info("<{}>在{}中切换并关闭{}类型的弹框".format(sys._getframe().f_code.co_name, img_doc, alert_type))
            start_time = time.time()
            WebDriverWait(self.driver, timeout, frequency).until(EC.alert_is_present())
            if alert_type in ['alert', 'confirm']:
                self.driver.switch_to.alert.accept()
            elif alert_type == 'prompt':
                self.driver.switch_to.alert.send_keys(text)
                self.driver.switch_to.alert.accept()
            else:
                case_logger.error("<{}>不支持{},请确认alert的类型".format(sys._getframe().f_code.co_name, alert_type))
        except Exception as e:
            case_logger.error("<{}>在{}中切换并关闭{}类型的弹框失败！".format(sys._getframe().f_code.co_name, img_doc, alert_type))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))
        else:
            end_time = time.time()
            case_logger.info("<{}>在{}中切换并关闭{}类型的弹框，等待时间：{}秒".
                             format(sys._getframe().f_code.co_name, img_doc, alert_type, round(end_time - start_time, 2)))

    def select_action(self, loc, img_doc, content, select_type, timeout=20, frequency=0.5):
        """
        Select操作
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param content: select_by_方法的入参
        :param select_type: select类型
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        """
        self.wait_ele_to_click(loc, img_doc, timeout, frequency)
        try:
            case_logger.info("<{}>在{}上根据元素<{}>以{}方式进行下拉选择".format(sys._getframe().f_code.co_name, img_doc, loc, select_type))
            ele = self.get_ele(loc, img_doc)
            if select_type == 'index':
                Select(ele).select_by_index(content)
            elif select_type == 'value':
                Select(ele).select_by_value(content)
            elif select_type == 'text':
                Select(ele).select_by_visible_text(content)
            else:
                case_logger.error("<{}>不支持{},请确认Select的类型".format(sys._getframe().f_code.co_name, select_type))
        except Exception as e:
            case_logger.error("<{}>在{}上根据元素<{}>以{}方式进行下拉选择失败！".format(sys._getframe().f_code.co_name, img_doc, loc, select_type))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))

    def switch_to_windows(self, loc, img_doc, timeout=20, frequency=0.5):
        """
        窗口切换
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        """
        try:
            case_logger.info("<{}>在{}中根据元素<{}>进行窗口切换".format(sys._getframe().f_code.co_name, img_doc, loc))
            cur_handles = self.driver.window_handles  # 获取点击之前的窗口总数
            start_time = time.time()
            self.click_ele(loc, img_doc, timeout, frequency)  # 点击按钮后新的窗口出现
            WebDriverWait(self.driver, timeout, frequency).until(EC.new_window_is_opened(cur_handles))
            wins = self.driver.window_handles  # 再次获取窗口总数
            self.driver.switch_to.window(wins[-1])  # 切换到新的页面
        except Exception as e:
            case_logger.error("<{}>在{}中根据元素<{}>进行窗口切换失败！".format(sys._getframe().f_code.co_name, img_doc, loc))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("<{}>错误信息<{}>".format(sys._getframe().f_code.co_name, e))
        else:
            end_time = time.time()
            case_logger.info("<{}>在{}中根据元素<{}>进行窗口切换，等待时间：{}秒".
                             format(sys._getframe().f_code.co_name, img_doc, loc, round(end_time - start_time, 2)))

    def wait_ele_to_visible(self, loc, img_doc, timeout=20, frequency=0.5):
        """
        等待元素可见
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        """
        try:
            case_logger.info("[{}]<{}>开始等待页面元素<{}>是否可见！".format(img_doc, sys._getframe().f_code.co_name, loc))
            start_time = time.time()
            WebDriverWait(self.driver, timeout, frequency).until(EC.visibility_of_element_located(loc))
        except Exception as e:
            case_logger.error("[{}]<{}>页面元素<{}>等待可见失败！".format(img_doc, sys._getframe().f_code.co_name, loc))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))
        else:
            end_time = time.time()
            case_logger.info("[{}]<{}>页面元素<{}>等待可见，等待时间：{}秒".format(img_doc, sys._getframe().f_code.co_name, loc, round(end_time - start_time, 2)))

    def wait_ele_to_click(self, loc, img_doc, timeout=20, frequency=0.5):
        """
        等待元素可点击
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        """
        try:
            case_logger.info("[{}]<{}>开始等待页面元素<{}>是否可点击！".format(img_doc, sys._getframe().f_code.co_name, loc))
            start_time = time.time()
            WebDriverWait(self.driver, timeout, frequency).until(EC.element_to_be_clickable(*loc))
        except Exception as e:
            case_logger.error("[{}]<{}>页面元素<{}>等待可点击失败！".format(img_doc, sys._getframe().f_code.co_name, loc))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))
        else:
            end_time = time.time()
            case_logger.info("[{}]<{}>页面元素<{}>等待可点击，等待时间：{}秒".format(img_doc, sys._getframe().f_code.co_name, loc, round(end_time - start_time, 2)))

    def wait_element_to_be_exist(self, loc, img_doc, timeout=20, frequency=0.5):
        """
        等待元素存在
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        """
        try:
            case_logger.info("[{}]<{}>开始等待页面元素<{}>是否存在！".format(img_doc, sys._getframe().f_code.co_name, loc))
            start_time = time.time()
            WebDriverWait(self.driver, timeout, frequency).until(EC.presence_of_element_located(*loc))
        except Exception as e:
            case_logger.error("[{}]<{}>页面元素<{}>等待存在失败！".format(img_doc, sys._getframe().f_code.co_name, loc))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))
        else:
            end_time = time.time()
            case_logger.info("[{}]<{}>页面元素<{}>等待存在，等待时间：{}秒".format(img_doc, sys._getframe().f_code.co_name, loc, round(end_time - start_time, 2)))

    def save_screenshot(self, img_doc):
        """
        页面截屏保存截图
        :param img_doc: 截图说明
        :return:
        """
        # print(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
        file_name = PIC_DIR + r"\{}_{}.png".format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()), img_doc)
        # print(file_name)
        self.driver.save_screenshot(file_name)
        with open(file_name, mode='rb') as f:
            file = f.read()
        allure.attach(file, img_doc, allure.attachment_type.PNG)
        case_logger.info("[{}]<{}>截图保存在：{}".format(img_doc, sys._getframe().f_code.co_name, file_name))

    def get_ele(self, loc, img_doc):
        """
        获取页面中的元素
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :return: WebElement对象
        """
        self.wait_ele_to_visible(loc, img_doc, timeout=20, frequency=0.5)
        try:
            # self.clear_text(loc, img_doc)
            # self.driver.find_element(*loc).clear()
            case_logger.info("[{}]<{}>查找元素<{}>".format(img_doc, sys._getframe().f_code.co_name, loc))
            ele = self.driver.find_element(*loc)
        except Exception as e:
            case_logger.error("[{}]<{}>查找元素<{}>失败！".format(img_doc, sys._getframe().f_code.co_name, loc))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))
        else:
            # print("<{}>返回值是<{}>".format(sys._getframe().f_code.co_name, ele))
            return ele

    def get_eles(self, loc, img_doc):
        """
        获取页面中的所有元素
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :return: WebElement对象
        """
        self.wait_ele_to_visible(loc, img_doc, timeout=20, frequency=0.5)
        try:
            case_logger.info("[{}]<{}>查找所有元素<{}>".format(img_doc, sys._getframe().f_code.co_name, loc))
            # self.clear_text(loc, img_doc)
            ele = self.driver.find_elements(*loc)
        except Exception as e:
            case_logger.error("[{}]<{}>查找所有元素<{}>失败！".format(img_doc, sys._getframe().f_code.co_name, loc))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))
        else:
            # case_logger.info("<{}>返回值是<{}>".format(sys._getframe().f_code.co_name, ele))
            return ele

    def input_text(self, loc, text, img_doc, timeout=20, frequency=0.5):
        """
        对输入框输入文本内容
        :param text: 输入的文本内容
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        """
        self.wait_ele_to_visible(loc, img_doc, timeout, frequency)
        try:
            self.driver.find_element(*loc).clear()
            self.driver.find_element(*loc).send_keys(text)
            # self.get_ele(loc, img_doc).send_keys(text)
            case_logger.info("[{}]<{}>输入元素<{}>的内容为<{}>".format(img_doc, sys._getframe().f_code.co_name, loc, text))
        except Exception as e:
            case_logger.error("[{}]<{}>在元素<{}>中输入内容<{}>失败！".format(img_doc, sys._getframe().f_code.co_name, loc, text))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))

    def clear_text(self, loc, img_doc, timeout=20, frequency=0.5):
        """
        清除文本框的内容
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        """
        self.wait_ele_to_visible(loc, img_doc, timeout, frequency)
        try:
            # self.get_ele(loc, img_doc).clear()
            case_logger.info("[{}]<{}>清除元素<{}>的文本内容".format(img_doc, sys._getframe().f_code.co_name, loc))
            self.driver.find_element(*loc).clear()
        except Exception as e:
            case_logger.error("[{}]<{}>清除元素<{}>的文本内容失败！".format(img_doc, sys._getframe().f_code.co_name, loc))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))

    def click_ele(self, loc, img_doc, timeout=20, frequency=0.5):
        """
        点击按钮
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return:
        """
        #self.wait_ele_to_click(loc, img_doc, timeout, frequency)
        self.wait_ele_to_visible(loc, img_doc, timeout, frequency)
        try:
            # self.get_ele(loc, img_doc).click()
            case_logger.info("[{}]<{}>点击元素<{}>".format(img_doc, sys._getframe().f_code.co_name, loc))
            self.driver.find_element(*loc).click()
            # self.get_ele(loc, img_doc).click()
        except Exception as e:
            case_logger.error("[{}]<{}>点击元素<{}>失败！".format(img_doc, sys._getframe().f_code.co_name, loc))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))

    def get_ele_text(self, loc, img_doc, timeout=20, frequency=0.5):
        """
        获取WebElement对象的文本值
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return: WebElement对象的文本值
        """
        self.wait_ele_to_visible(loc, img_doc, timeout, frequency)
        try:
            # text = self.get_ele(loc, img_doc).text
            case_logger.info("[{}]<{}>获取元素<{}>的文本值".format(img_doc, sys._getframe().f_code.co_name, loc))
            text = self.driver.find_element(*loc).text
        except Exception as e:
            case_logger.error("[{}]<{}>获取元素<{}>的文本值失败！".format(img_doc, sys._getframe().f_code.co_name, loc))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))
        else:
            case_logger.info("[{}]<{}>返回值为【{}】".format(img_doc, sys._getframe().f_code.co_name, text))
            return text

    def get_eles_text(self, loc, img_doc, timeout=20, frequency=0.5):
        """
        获取WebElement对象的所有文本值
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return: WebElement对象的文本值的列表
        """
        self.wait_ele_to_visible(loc, img_doc, timeout, frequency)
        try:
            # all_text = self.get_eles(loc, img_doc)
            case_logger.info("[{}]<{}>获取元素<{}>的所有文本值".format(img_doc, sys._getframe().f_code.co_name, loc))
            all_text = self.driver.find_elements(*loc).text
            text_list = []
            for one_text in all_text:
                text_list.append(one_text.text)
        except Exception as e:
            case_logger.error("[{}]<{}>获取元素<{}>的所有文本值失败！".format(img_doc, sys._getframe().f_code.co_name, loc))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))
        else:
            case_logger.info("[{}]<{}>返回值为<{}>".format(img_doc, sys._getframe().f_code.co_name, text_list))
            return text_list

    def get_ele_attr(self, attr_name, loc, img_doc, timeout=20, frequency=0.5):
        """
        获取WebElement对象的属性值
        :param attr_name: 属性名称
        :param loc: 元素定位的XPATH元组表达式
        :param img_doc: 截图说明
        :param timeout: 等待的超时时间
        :param frequency: 轮询频率
        :return: WebElement对象的属性值
        """
        self.wait_element_to_be_exist(loc, img_doc, timeout, frequency)
        try:
            # value = self.get_ele(loc, img_doc).get_attribute(attr_name)
            case_logger.info("[{}]<{}>获取元素<{}>的属性<{}>的值".format(img_doc, sys._getframe().f_code.co_name, loc, attr_name))
            value = self.driver.find_element(*loc).get_attribute(attr_name)
        except Exception as e:
            case_logger.error("[{}]<{}>获取元素<{}>的属性<{}>的值失败！".format(img_doc, sys._getframe().f_code.co_name, loc, attr_name))
            self.save_screenshot(img_doc)
            raise e
            case_logger.error("[{}]<{}>错误信息<{}>".format(img_doc, sys._getframe().f_code.co_name, e))
        else:
            case_logger.info("[{}]<{}>获取到的元素属性值为<{}>".format(img_doc, sys._getframe().f_code.co_name, value))
            return value
