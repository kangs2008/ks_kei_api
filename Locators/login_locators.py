# from selenium.webdriver.common.by import By
XPATH = 'xpath'
ID = 'id'
var ={}
def _get_variables(page):
    if page == 'login_page':
        username_loc = { 'loc': '//input[@name = "phone"]',
                         't': XPATH, 'info': f'{page}|用户名'}
        var['username_loc'] = username_loc

        password_loc = {'loc': '//input[@name = "password"]',
                        't': XPATH, 'info': f'{page}|密码'}
        var['password_loc'] = password_loc

        login_btn_loc = {'loc': '//button[@class = "btn btn-special"]',
                        't': XPATH, 'info': f'{page}|登录按钮'}
        var['login_btn_loc'] = login_btn_loc

        error_msg_loc = {'loc': '//button[@class = "form-error-info"]',
                        't': XPATH, 'info': f'{page}|all错误'}
        var['error_msg_loc'] = error_msg_loc

        user_msg_loc = {'loc': '//*[@class = "login-form"]/form/div[1]/div',
                        't': XPATH, 'info': f'{page}|user错误信息'}
        var['user_msg_loc'] = user_msg_loc

        pwd_msg_loc = {'loc': '//*[@class = "login-form"]/form/div[2]/div',
                        't': XPATH, 'info': f'{page}|pwd错误信息'}
        var['pwd_msg_loc'] = pwd_msg_loc
        return var
    elif page == 'home_page':
        pass
        return var
    else:
        print('wrong!!!!')
        return var

def loc_info(page, loc_name):
    one_loc = _get_variables(page)
    loc = one_loc[loc_name]['loc']
    # print(loc)
    t = one_loc[loc_name]['t']
    # print(t)
    info = one_loc[loc_name]['info']
    # print(info)
    return t, loc, info
    # return t, loc

if __name__ == '__main__':
    a = loc_info('login_page', 'username_loc')
    print(a[-1])
    print(a)
    print(a[:-1])

# class LoginLocator:
#     username_loc = (By.XPATH, '//input[@name = "phone"]')
#     password_loc = (By.XPATH, '//input[@name = "password"]')
#     login_btn_loc = (By.XPATH, '//button[@class = "btn btn-special"]')
#     error_msg_loc = (By.XPATH, '//button[@class = "form-error-info"]')
#     user_msg_loc = (By.XPATH, '//*[@class = "login-form"]/form/div[1]/div')
#     pwd_msg_loc = (By.XPATH, '//*[@class = "login-form"]/form/div[2]/div')
