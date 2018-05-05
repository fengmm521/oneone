#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-05-05 13:40:12
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os,sys
import time


serverPth = '/root/game/OneLife/server'
liftlogPth = serverPth + os.sep + 'lifeLog'


def getTodayFileName():
    timeArray = time.localtime(int(time.time()))
    otherStyleTime = time.strftime("%Y_%m%B_%d_%A", timeArray)
    print(otherStyleTime)
    return otherStyleTime

#获取服务器人数
def getServerPopCount():
    #D 1525497260 184 3429231435@QQ.COM age=20.63 F (6,-33) disconnect pop=0
    tfname = liftlogPth + os.sep + getTodayFileName() + '.txt'
    f = open(tfname,'r')
    lines = f.readlines()
    f.close()
    if lines:
        tmps = lines[-1].replace('\n','').split(' ')
        t = int(tmps[1])
        tstr = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(t)) 
        account = tmps[3]
        isB = tmps[0]
        popstr = ''
        if isB == 'B':
            popstr = tmps[-2]
        else:
            popstr = tmps[-1]
        pcount = popstr.split('=')[1]

        outstr = '%s,%s,%s,%s'%(tstr,isB,account,pcount)
        return outstr
    else:
        return 'today not data'

def main():
    pcount = getServerPopCount()
    pcount = pcount.replace(',', ' ')
    print(pcount)
#测试
if __name__ == '__main__':
    main()
    
