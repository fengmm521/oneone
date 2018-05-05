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

#获取脚本路径
def cur_file_dir():
    pathx = sys.argv[0]
    tmppath,_file = os.path.split(pathx)
    if cmp(tmppath,'') == 0:
        tmppath = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(tmppath):
        return tmppath
    elif os.path.isfile(tmppath):
        return os.path.dirname(tmppath)
    
#获取父目录
def GetParentPath(strPath):
    if not strPath:
        return None;
    lsPath = os.path.split(strPath);
    if lsPath[1]:
        return lsPath[0];
    lsPath = os.path.split(lsPath[0]);
    return lsPath[0];

def isRun(pid):
    strtmp = os.popen('/bin/ps axu|grep "%s"'%(pid)) 
    print type(strtmp)
    cmdback = strtmp.read()
    print cmdback
    cmdbacks = cmdback.split('\n')
    for c in cmdbacks:
        tmpstr = ' '.join(c.split())
        tmps = tmpstr.split(' ')
        if len(tmps) > 1 and tmps[1] == pid:
            return c
    return None

def getRunPID():

    rpidpth = serverPth + '/psid.txt'

    if not os.path.exists(rpidpth):
        return '-1'

    f = open(rpidpth,'r')
    lines = f.readlines()
    f.close()

    line = lines[1].replace('\n','')
    return str(line)

def reRunPSWithSH():
    shpth = GetParentPath(cur_file_dir()) + '/runoogame.sh'
    cmd = '/bin/sh %s'%(shpth)
    print(cmd)
    os.system(cmd)
#获取服务器人数
def getServerPopCount():
    #D 1525497260 184 3429231435@QQ.COM age=20.63 F (6,-33) disconnect pop=0
    tfname = liftlogPth + os.sep + getTodayFileName() + '.txt'
    f = open(tfname,'r')
    lines = f.readlines()
    f.close()
    if lines:
        pcount = lines[-1].replace('\n','').split(' ')[-1].split('=')[1]
        return int(pcount)

def main():

    runPID = getRunPID()

    while True:
        if isRun(runPID) == None:
            reRunPSWithSH()
            time.sleep(3)
            runPID = getRunPID()
            print('reurn at %s'%(time.ctime()))
        time.sleep(10)
        

def test():
    print(GetParentPath(cur_file_dir()))
    print('rerun at %s'%(time.ctime()))

#测试
if __name__ == '__main__':
    main()
    
