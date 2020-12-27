import os, sys
import time
from selenium import webdriver
import cv2
import unittest



d = webdriver.Chrome()
d.get('httP://www.baidu.com')
d.maximize_window()
size = d.get_window_size()
time.sleep(5)
print('size', size)

def paint_on_screenshot(pos, filename, h, hw):
    screenvc = cv2.imread(filename)
    sx = int(screenvc.shape[1])
    sy = int(screenvc.shape[0])
    print('sx, sy', sx, sy)

    ratex = sx / 1552
    ratey = sy / 840

    pos = (int(int(pos[0]) * ratex), int(int(pos[1]) * ratey))
    # screenvc = cv2.resize(screenvc, (1920, 889))
    img_res = cv2.circle(screenvc, pos, 15, (0, 0, 225), 3)

    cv2.imwrite(filename, img_res)

def paint_on_screenshot2(pos, filename, h, hw):
    screenvc = cv2.imread(filename)
    sx = int(screenvc.shape[1])
    sy = int(screenvc.shape[0])
    print('sx, sy', sx, sy)

    # ratex = 1920 / sx
    # ratey = 1080 / sy
    #
    # pos = (int(int(pos[1]) * ratex), int(int(pos[0]) * ratey))
    # screenvc = cv2.resize(screenvc, (1920, 889))
    img_res = cv2.circle(screenvc, pos, 20, (0, 0, 225), 2)

    cv2.imwrite(filename, img_res)

lo = d.find_element_by_id('su').location
print(lo)
lx = lo['x']
ly = lo['y']

input = d.find_element_by_id('su').size
print(input)
h = input['height']
hw = input['width']

p_x = int(int(h) / 2)
p_y = int(int(hw) / 2)


pos_xx = int(lx) + p_y
pos_yy = int(ly) + p_x

# pos_xx = int(lx)
# pos_yy = int(ly)


print(pos_xx, pos_yy)
time.sleep(1)
f = r'D:\desk20201127\a.png'
d.save_screenshot(f)

paint_on_screenshot((pos_xx, pos_yy), f, h, hw)


d.find_element_by_id('su')




# win_size = d.get_window_size()
# print(win_size)
#
# w = win_size['width']
# wh = win_size['height']