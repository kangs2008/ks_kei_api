
valid_user = ("18684720553", "python")

invalid_data = [
    {"user":"", "passwd":"python", "check":"请输入手机号"},
    {"user":"18684720553", "passwd":"", "check":"请输入密码"},
    {"user":"1868472055", "passwd":"python", "check":"请输入正确的手机号"},
    {"user":"186847205531", "passwd":"python", "check":"请输入正确的手机号"}
]