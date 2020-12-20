import csv


class HandleCsv:
    '''
    csv文件处理类
    '''
    def __init__(self, filename):
        '''
        构造器
        :param filename: csv文件名
        '''
        self.filename = filename

    def get_data(self):
        '''
        获取csv中所有数据
        :return: 嵌套字典的列表
        '''
        with open(self.filename, mode='r', encoding='utf-8') as f:
            cb = csv.reader(f)  # 实例化reader对象
            header = next(cb)  # 获取表头，并将指针转向下一行
            list_dict = []
            for row in cb:
                list_dict.append(dict(zip(header, row)))
        return list_dict

    def get_one_row(self, row):
        '''
        获取单行数据
        :param row: 指定的行号
        :return: 对应行号的数据
        '''
        return self.get_data()[row - 1]

    def write_csv(self, headers, values, data_type, mode='w'):
        '''
        写入数据到csv到文件中
        :param headers: 表头：列表类型
        :param values: 表数据：1.嵌套元组的列表；2.嵌套字典的列表
        :param data_type: 传入的数据类型：1.'tuple'；2.'dict'
        :param mode: 写入方式，默认写入“w”
        :return:
        '''
        with open(file=self.filename, mode=mode, encoding='utf-8', newline='') as f:
            if data_type == 'tuple':
                writer = csv.writer(f)  # 实例化writer对象
                writer.writerow(headers)  # 写入表头
                writer.writerows(values)  # 写入数据
            elif data_type == 'dict':
                writer = csv.DictWriter(f, headers)  # 实例化DictWriter对象
                writer.writeheader()  # 写入表头
                writer.writerows(values)  # 写入数据
            else:
                print("数据类型错误，请确认！")