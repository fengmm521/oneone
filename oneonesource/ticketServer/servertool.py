#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-22 09:44:42

import time
import os



class ServerUser(object):
    """docstring for ClassName"""
    def __init__(self, logdir = '/root/game/OneLife/server/lifeLog'):
        self.logfiledir =    logdir        
        self.lines = []
    def getTodayFileName(self):
        timeArray = time.localtime(int(time.time()))
        otherStyleTime = time.strftime("%Y_%m%B_%d_%A", timeArray)
        print(otherStyleTime)
        return otherStyleTime

    def getServerLogLines(self):
        logfpth = self.logfiledir + os.sep + self.getTodayFileName() + '.txt'
        f = open(logfpth)
        self.lines = f.readlines()
        f.close()

    def getServerData(self):
        self.getServerLogLines()
        count = 0
        users = []
        accountcount = {}
        if self.lines:
            for l in self.lines:
                if len(l) < 10:
                    continue
                tmps = l.replace('\n','').split(' ')
                account = tmps[3]
                t = int(tmps[1])
                tstr = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime(t)) 
                isB = tmps[0]
                age = '0'
                fposion = ''
                playerstat = 'B'
                popstr = ''
                parent = 'noParent'
                if isB == 'B':
                    popstr = tmps[-2]
                    fposion = tmps[5]             #生出坐标
                    if tmps[6] != 'noParent':
                        parent = tmps[6].split(',')[1]
                else:
                    popstr = tmps[-1]
                    age = tmps[4].split('=')[1]   #死亡年龄
                    fposion = tmps[6]             #死亡坐标
                    playerstat = tmps[7]          #死亡原因
                countplayer = popstr.split('=')[1]
                if account in accountcount:
                    accountcount[account] += 1
                else:
                    accountcount[account] = 1
                users.append([account,isB,tstr,age,fposion,playerstat,countplayer,parent])
        minxing = 0
        minxinguser = ''
        for k in accountcount.keys():
            if accountcount[k] > minxing:
                minxing = accountcount[k]
                minxinguser = k
        if len(users) > 30:
            users = users[-30:]
        return users,minxinguser

    #获取服务器状态
    def getServerStat(self):
        users,minxinguser = self.getServerData()
        count = str(users[-1][6])
        return count,minxinguser,users



def test():
    pass

if __name__=="__main__":  
    test()

