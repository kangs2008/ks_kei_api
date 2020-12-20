import pymysql


class HandleMysql:
    """
    定义一个mysql处理类
    """

    def __init__(self, hostname, username, password, database_name, port=3306):
        '''
        建立数据库连接并创建字典类型游标
        '''
        self.conn = pymysql.connect(
            host=hostname,  # 主机名
            user=username,  # 用户名
            password=password,  # 密码
            db=database_name,  # 数据库名
            port=port,  # 端口号
            charset='utf8',  # 字符集
            cursorclass=pymysql.cursors.DictCursor  # 游标类型
        )
        self.cursor = self.conn.cursor()  # 创建游标

    def run(self, sql, args=None, is_more=False):
        '''
        执行sql语句
        :param sql:sql语句
        :param args:元组类型可变参数（用于sql语句字符串中的占位符填充时传参使用）
        :param is_more:默认False为执行一条sql语句
        :return:sql语句执行结果（fetchone()返回的是一个字典，fetchall()返回的是一个嵌套字典的列表）
        '''
        self.cursor.execute(sql, args=args)  # 执行sql语句
        self.conn.commit()  # 提交sql语句
        if is_more:
            return self.cursor.fetchall()  # 获取多个执行结果
        else:
            return self.cursor.fetchone()  # 获取一条执行结果

    def close(self):
        '''
        关闭连接
        '''
        self.cursor.close()  # 关闭游标
        self.conn.close()  # 关闭数据库