# api_allure         作者:kangs2008

## 版本：V 1.0
### 更新说明：
- 只保留API使用的文件：

## 项目说明
- 本框架是一套数据驱动自动化接口框架,基于**excel+requests+pytest+allure**设计,本框架无需你使用代码编写用例,一切将在EXCEL中进行！！本框架实现了在EXCEL中
进行**接口用例编写,接口关联,接口断言**,同时支持传统python代码编写测试case方式。
- 入口支持传入参数，可执行要执行excel文件，或文件夹，或某个excel sheet，以及指定以日期方式生成报告文件夹/以年月日时分秒方式生成报告文件夹
- excel文件可指定任意行为需要执行的行
- 报告文件写入excel

## 技术栈
- requests
- pytest
- pytest-html
- pytest-allure
- openpyxl
- logging

## 项目结构说明
- Common ===========> 工具文件
- Apikeywords.apiKeyWords ===========> 核心工具类等
- Datas ==========> excel测试数据
- Logs ==========> 自增log文件
- Report ==========> 测试报告文件
- temp ==========> allure报告使用的临时文件
- TsetCases ===========> API测试用例
- requirements.txt ============> 相关依赖包文件
- conftest.py =============> create session
- exec_ini.py =============> write ini file
- README.md ============> 项目说明文档
- runner_allure.py ============> allure报告生成
- runner_html.py ============> html报告生成
- runner_py.py ============> 以python方式编写测试用例

## EXCEL字段说明
- **num**:用例番号
- **exec**:该行是否被执行（被编写到测试用例中）
- **title**:表明接下来要执行的某个方法名字
- **method**:所有已经编写好的方法（get，post，assert。。。）
- **input**:执行该method需要输入的字段
- **request_data**:执行该method需要输入的body
- **status**:自定义
- **expext**:自定义
- **return_code**:执行后，写入excel的字段1
- **return_value**:执行后，写入excel的字段2

## 关联详解
- savedata：写入参数池（自定义需要的数据）
- savejson：写入参数池（从post、get等返回的res来取得数据写入参数池）
- saveparam：写入参数池（为get方法传参）

## 断言
- 支持绝对路径判断，支持相对路径判断

## 后续
- 根据要测试接口需要，可增加sql等方法和各种工具，完善该接口

## 截图
`https://github.com/kangs2008/api_allure/blob/master/Sn.png`截图