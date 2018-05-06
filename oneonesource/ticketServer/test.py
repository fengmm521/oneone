#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time
import platform
import requests
import base64
import hashlib

import rsa

from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding( "utf-8" )

# python中时间日期格式化符号：
# %y 两位数的年份表示（00-99）
# %Y 四位数的年份表示（000-9999）
# %m 月份（01-12）
# %d 月内中的一天（0-31）
# %H 24小时制小时数（0-23）
# %I 12小时制小时数（01-12）
# %M 分钟数（00=59）
# %S 秒（00-59）
# %a 本地简化星期名称
# %A 本地完整星期名称
# %b 本地简化的月份名称
# %B 本地完整的月份名称
# %c 本地相应的日期表示和时间表示
# %j 年内的一天（001-366）
# %p 本地A.M.或P.M.的等价符
# %U 一年中的星期数（00-53）星期天为星期的开始
# %w 星期（0-6），星期天为星期的开始
# %W 一年中的星期数（00-53）星期一为星期的开始
# %x 本地相应的日期表示
# %X 本地相应的时间表示
# %Z 当前时区的名称
# %% %号本身


#https://blog.csdn.net/xiaobing_blog/article/details/12591917

def test():
    a = "2018_05May_01_Tuesday"
    # 将其转换为时间数组
    import time
    timeArray = time.strptime(a, "%Y_%m%B_%d_%A")
    # 转换为时间戳:
    timeStamp = int(time.mktime(timeArray))
    print(timeStamp)

def today():
    # timeStamp = 1381419600
    timeArray = time.localtime(int(time.time()))
    otherStyleTime = time.strftime("%Y_%m%B_%d_%A", timeArray)
    print(otherStyleTime)

#测试
if __name__ == '__main__':
    # main()
    test()
    today()




