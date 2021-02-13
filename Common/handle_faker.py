from faker import Faker


class RandomData:
    """
    生成随机测试数据
    """

    def __init__(self):
        self.f = Faker(locale='zh_CN')  # zh_CN代表中文，不传locale默认值为en_US

    def random_name(self):
        """
        随机姓名
        :return:
        """
        return self.f.name()

    def random_username(self):
        """
        随机用户名
        :return:
        """
        return self.f.user_name()

    def random_password(self, length=10, special_chars=True, digits=True, upper_case=True, lower_case=True):
        """
        随机密码
        :param length: 密码长度
        :param special_chars: 是否可使用特殊字符
        :param digits: 是否包含数字
        :param upper_case: 是否包含大写字母
        :param lower_case: 是否包含小写字母
        :return:
        """
        return self.f.password(length=length,
                               special_chars=special_chars,
                               digits=digits,
                               upper_case=upper_case,
                               lower_case=lower_case)

    def random_mobile_phone_num(self):
        """
        随机手机号
        :return:
        """
        return self.f.phone_number()

    def random_id_card_num(self):
        """
        随机身份证号
        :return:
        """
        return self.f.ssn()

    def random_email(self):
        """
        随机邮箱
        :return:
        """
        return self.f.email()

    def random_address(self):
        """
        随机地址
        :return:
        """
        return self.f.address()

    def random_url(self):
        """
        随机url
        :return:
        """
        return self.f.url()

    def random_ipv4(self):
        """
        随机ipv4（IP号）
        :return:
        """
        return self.f.ipv4()

    def random_md5(self):
        """
        随机MD5加密串
        :return:
        """
        return self.f.md5()
print(RandomData().random_name())
print(RandomData().random_username())
# f.name() 生成姓名
# f.address() 生成地址
# city_suffix() 市/县
# country() 国家
# country_code() 国家编码
# district() 区
# geo_coordinate() 地理坐标
# latitude() 地理坐标(纬度)
# longitude() 地理坐标(经度)
# lexify() 替换所有问号（“？”）带有随机字母的事件
# numerify() 三位随机数字
# postcode() 邮编
# province() 省份
# street_address() 街道地址
# street_name() 街道名
# street_suffix() 街/路
# random_digit() 0~9随机数
# random_digit_not_null() 1~9的随机数
# random_element() 随机字母
# random_int() 随机数字，默认0~9999，可以通过设置min,max来设置
# random_letter() 随机字母
# random_number() 随机数字，参数digits设置生成的数字位数
# color_name() 随机颜色名
# hex_color() 随机HEX颜色
# rgb_color() 随机RGB颜色
# safe_color_name() 随机安全色名
# safe_hex_color() 随机安全HEX颜色
# bs() 随机公司服务名
# company() 随机公司名（长）
# company_prefix() 随机公司名（短）
# company_suffix() 公司性质
# credit_card_expire() 随机信用卡到期日
# credit_card_full() 生成完整信用卡信息
# credit_card_number() 信用卡号
# credit_card_provider() 信用卡类型
# credit_card_security_code() 信用卡安全码
# currency_code() 货币编码
# am_pm() AM/PM
# century() 随机世纪
# date() 随机日期
# date_between() 随机生成指定范围内日期，参数：start_date，end_date取值：具体日期或者today,-30d,-30y类似
# date_between_dates() 随机生成指定范围内日期，用法同上
# date_object() 随机生成从1970.1.1到指定日期的随机日期
# date_this_month() 随机本月日期
# date_this_year() 随机本年日期
# date_time() 随机生成指定时间（1970年1月1日至今）
# date_time_ad() 生成公元1年到现在的随机时间
# date_time_between() 用法同dates
# future_date() 未来日期
# future_datetime() 未来时间
# month() 随机月份
# month_name() 随机月份（英文）
# past_date() 随机生成已经过去的日期
# past_datetime() 随机生成已经过去的时间
# time() 随机24小时时间
# timedelta() 随机获取时间差
# time_object() 随机24小时时间，time对象
# time_series() 随机TimeSeries对象
# timezone() 随机时区
# unix_time() 随机Unix时间
# year() 随机年份
# file_extension() 随机文件扩展名
# file_name() 随机文件名（包含扩展名，不包含路径）
# file_path() 随机文件路径（包含文件名，扩展名）
# mime_type() 随机mime Type
# ascii_company_email() 随机ASCII公司邮箱名
# ascii_email() 随机ASCII邮箱
# ascii_free_email() 随机ASCII免费邮箱
# ascii_safe_email() 随机ASCII安全邮箱
# company_email() 随机公司邮箱
# domain_name() 生成域名
# domain_word() 域词(不包含后缀)
# email() 随机邮箱
# free_email() 免费邮箱
# free_email_domain() 免费邮箱后缀（如：yahoo.com）
# safe_email() 安全邮箱
# image_url() 随机URL地址
# ipv4() 随机IP4地址
# ipv6() 随机IP6地址
# mac_address() 随机MAC地址
# tld() 网址域名后缀(.com/.net/.cn等，不包括.)
# uri() 随机URI地址
# uri_extension() 网址文件后缀
# uri_page() 网址文件（不包含后缀）
# uri_path() 网址文件路径（不包含文件名）
# url() 随机URL地址
# user_name() 随机用户名
# isbn10() 随机ISBN（10位）
# isbn13() 随机ISBN（13位）
# job() 随机职位
# paragraph() 随机生成一个段落
# paragraphs() 随机生成多个段落，通过参数nb来控制段落数，返回数组
# sentence() 随机生成一句话
# sentences() 随机生成多句话，与段落类似
# text() 随机生成一篇文章
# word() 随机生成词语
# words() 随机生成多个词语，用法与段落，句子，类似
# binary() 随机生成二进制编码
# boolean() True/False
# language_code() 随机生成两位语言编码
# locale() 随机生成语言/国际信息
# md5() 随机生成MD5
# null_boolean() NULL/True/False
# password() 随机生成密码,可选参数：length：密码长度；special_chars：是否能使用特殊字符；
# -->digits：是否包含数字；upper_case：是否包含大写字母；lower_case：是否包含小写字母

# sha1() 随机SHA1
# sha256() 随机SHA256
# uuid4() 随机UUID
# first_name() 名
# first_name_female() 女性名
# first_name_male() 男性名
# first_romanized_name() 罗马名
# last_name() 姓
# last_name_female() 女姓
# last_name_male() 男姓
# last_romanized_name() 罗马姓
# name() 随机生成全名
# name_female() 男性全名
# name_male() 女性全名
# romanized_name() 罗马名
# msisdn() 移动台国际用户识别码，即移动用户的ISDN号码
# phone_number() 随机生成手机号
# phonenumber_prefix() 随机生成手机号段
# profile() 随机生成档案信息
# simple_profile() 随机生成简单档案信息
# pybool() 随机生成布尔值
# pydecimal() 随机生成decimal数字
# pydict() 随机生成字典
# pyfloat() 随机生成浮点数
# pyint() 随机生成整数
# pyiterable() 随机生成元组/列表/集合
# pylist() 随机生成列表
# pyset() 随机生成集合
# pystr() 随机生成字符串
# pystruct() 随机生成嵌套结构数据
# pytuple() 随机生成元组
# ssn() 生成身份证号
# chrome() 随机生成Chrome的浏览器user_agent信息
# firefox() 随机生成FireFox的浏览器user_agent信息
# internet_explorer() 随机生成IE的浏览器user_agent信息
# opera() 随机生成Opera的浏览器user_agent信息
# safari() 随机生成Safari的浏览器user_agent信息
# linux_platform_token() 随机Linux信息
# user_agent() 随机user_agent信息