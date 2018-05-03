#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-22 09:44:42

import dbm
import json
import time
import base64
import os
import hashlib
import hmac


class DBINIObj(object):
    """docstring for ClassName"""
    def __init__(self, pth):
        self.userpth = './db/user.txt'            #保存用户邮箱和密码
        self.userLoginIPPth = './db/userIP'       #保存用户IP和登陆时间文件名使用用户邮箱作为文件名

        self.userdics = {}                        #这里保存用户名和密码
        self.popcount = 0                         #服务器内的玩家数
        self.deadList = {}                        #这里保存玩家都是怎么死的，死亡时间，死亡坐标，死亡年龄

    def get_authorization(pwd, msg):  
        hashing = hmac.new(pwd, msg, hashlib.sha1).hexdigest()  
        return hashing  

    def saveUser(self):
        try:
            outjson = json.dumps(self.userdics)
        except Exception as e:
            return False

        cmd = 'mv -f ./db/user.txt ./db/userback.txt'   #备份一下原来的用户名
        os.system(cmd)
        f = open(self.userpth,'w')
        f.write(outjson)
        f.close()
        return True


    def addUser(self,email,pwd,clientIP):
        if email in self.userdics:
            return 1                              #返回值说明,0:添加完成,1:邮件已存在,2:密码太短，需要最少8位,-1:邮箱填写错误
        
        if len(pwd) < 8:
            return 2                              

        self.userdics[email] = base64.encode(pwd)
        if self.saveUser():
            return 0
        else:
            self.userdics.pop(email)
            return -1


    def userLogin(self,email,keyHash,msg,clientIP):
        isPass = False
        if email in self.userdics:
            upwd = self.userdics[email]
            turehash = self.get_authorization(upwd,msg)
            if keyHash == turehash:
                isPass = True

        return isPass
        

    def removeUser(self,email,pwd,clientIP):
        self.userdics.pop(email)
        self.saveUser()

    def getTodayFileName(self):
    # timeStamp = 1381419600
        timeArray = time.localtime(int(time.time()))
        otherStyleTime = time.strftime("%Y_%m%B_%d_%A", timeArray)
        # print(otherStyleTime)
        return otherStyleTime

    def initLifeLog(self):
        fname = self.getTodayFileName()
        fpth = fname + '.txt'
        f = open(fname,'r')
        lines = f.readlines()
        f.close()

    def getUserCount(self):
        

    def getDeadList(self):
        pass

    def getUserDeadList(self,email):
        pass

def main():
    pass

if __name__=="__main__":  
    main()

