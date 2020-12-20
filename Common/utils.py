import allure
import time, datetime
import time

def mTime():
    return str(datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3])

def formatTime():
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

def assertTrueMethod(actual_msg, expect_msg):
    m = mTime()
    with allure.step(f"[{m}][assert]方法, 实际值：<{actual_msg}>, 期望值：<{expect_msg}>"):
        assert actual_msg == expect_msg


def assertFalseMethod(actual_msg, expect_msg):
    m = mTime()
    with allure.step(f"[{m}][assert]方法, 实际值：<{actual_msg}>, 期望值：<{expect_msg}>"):
        assert actual_msg != expect_msg

def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print (otherStyleTime)


def use_time(starttime, endtime):
    # starttime = time.time()
    # endtime = time.time()
    m, s = divmod(int(endtime - starttime), 60)
    h, m = divmod(m, 60)
    return "测试使用时间 %d:%02d:%02d" % (h, m, s)

def start_time_format(starttime):
    return time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(starttime)) # time.localtime(time.time())

if __name__ == '__main__':
    print(mTime())
    print(start_time_format())