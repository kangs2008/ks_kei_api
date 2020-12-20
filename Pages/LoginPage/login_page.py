import allure
import sys
from Locators.login_locators import loc_info as loc
from Common.basepage import BasePage
from Common.utils import mTime

class LoginPage(BasePage):

    # 登录
    def return_value(self, value):
        with allure.step(f"返回值是：[{value}]"):
            pass


    # 登录
    @allure.step("登录Method")
    def login(self, username, pwd):
        self.input_username(username)
        self.input_pwd(pwd)
        self.login_btn()

    # 获取错误提示
    def get_login_errMsg(self):
        m = sys._getframe().f_code.co_name
        locs = loc('login_page', 'error_msg_loc')
        with allure.step(f"[{mTime()}][{m}][{locs[-1]}]{locs[:-1]}"):
            value = self.get_ele_text(locs[:-1], m)
            print('这里是返回值显示')
            # allure.attach(f'返回值:[{value}]')
            allure.description('这返回值显示')
            return value

    def input_username(self, username):
        m = sys._getframe().f_code.co_name
        locs = loc('login_page', 'username_loc')
        with allure.step(f"[{mTime()}][{m}][{locs[-1]}][{username}]{locs[:-1]}"):
            self.input_text(locs[:-1], username, m)

    def get_user_errMsg(self):
        m = sys._getframe().f_code.co_name
        locs = loc('login_page', 'user_msg_loc')
        with allure.step(f"[{mTime()}][{m}][{locs[-1]}]{locs[:-1]}"):
            value = self.get_ele_text(locs[:-1], m)
            # allure.attach(f'返回值:[{value}]')
            print('这里是返回值显示')
            # allure.attach(f'返回值:[{value}]')
            self.return_value(value)

            return value

    def input_pwd(self, pwd):
        m = sys._getframe().f_code.co_name
        locs = loc('login_page', 'password_loc')
        with allure.step(f"[{mTime()}][{m}][{locs[-1]}][{pwd}]{locs[:-1]}"):
            self.input_text(locs[:-1], pwd, m)

    def get_pwd_errMsg(self):
        m = sys._getframe().f_code.co_name
        locs = loc('login_page', 'pwd_msg_loc')
        with allure.step(f"[{mTime()}][{m}][{locs[-1]}]{locs[:-1]}"):
            value = self.get_ele_text(locs[:-1], m)
            # allure.attach(f'返回值:[{value}]')
            self.return_value(value)
            return value

    def login_btn(self):
        m = sys._getframe().f_code.co_name
        locs = loc('login_page', 'login_btn_loc')
        with allure.step(f"[{mTime()}][{m}][{locs[-1]}]{locs[:-1]}"):
            self.click_ele(locs[:-1], m)
