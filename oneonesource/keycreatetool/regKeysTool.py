#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-07 09:28:00
# @Link    : http://fengmm521.blog.163.com
# @Version : $Id$
#https服务器
import os
import json
import time
import dbTool
import hashlib
import base58

class RegKeysTool(object):
    """docstring for WXMsgTool"""
    def __init__(self,dbpth = './db/regcode'):
        super(RegKeysTool, self).__init__()

        if not os.path.exists('db'):
            os.mkdir('db')

        if not os.path.exists(dbpth):
            os.mkdir(dbpth)


        #已付费注册用户
        self.dbPth = dbpth + os.sep + 'regcode'
        self.db = dbTool.DBMObj(self.dbPth)
        # self.regCodeObj = {}        #{regCode:{UUID:{硬件唯一码},os:{操作系统信息},hard:{硬件信息}}}


        #新生成的未使用注册码
        self.creagedbpth = dbpth + os.sep + 'create'
        self.createdb = dbTool.DBMObj(self.creagedbpth)

        # self.initRegCodeObj()


    # def initRegCodeObj(self):
        # self.regCodeObj = self.db.getDBDatas()

    #获取所有未使用的注册码
    def getNoAllRegCode(self):
        noregs = self.createdb.allKeys()
        return noregs

    #注册码和硬件注册
    def addHardMsgToRegDB(self,regCode,hardDic):
        tmpd = {}
        ctmp = self.createdb.select(regCode)
        if ctmp != None:
            tmpd = json.loads(ctmp)
            tmpd['hard'] = hardDic
            tmpd['rtime'] = int(time.time())
            jstr = json.dumps(tmpd)
            self.db.inset(regCode,jstr)
            self.createdb.delet(regCode)
            print(len(self.createdb.allKeys()))
            return True
        else:
            return False
    #获取注册硬件信息
    def getRegCodeData(self,regCode):
        dat = self.db.select(regCode)
        if dat != None:
            return json.loads(dat)
        else:
            return None
    #生成新的注册码
    def createRegistCode(self,count = 50):
        ks = []
        sendtmp = str(time.time())
        
        crcount = self.createdb.select('createcount')
        print(crcount)
        if crcount == None:
            crcount = 1
            self.createdb.inset('createcount', str(crcount))
        else:
            crcount = int(crcount) + 1
            self.createdb.inset('createcount', str(crcount))
        kfrontstr = base58.b58encode_int(crcount)
        if len(kfrontstr) == 1:
            kfrontstr = '0' + kfrontstr
        for i in range(count):
            tmpn = '0x' + hashlib.md5(sendtmp + str(i)).hexdigest()
            num = int(tmpn,16)
            bastr = base58.b58encode_int(num)
            tmpka = kfrontstr + bastr
            ks.append(tmpka)
        cdic = '{"cnum":%d}'%(crcount)
        vs = [cdic] * count
        isOK = self.createdb.insetList(ks, vs)
        jout = json.dumps(ks)
        return jout,isOK

if __name__ == '__main__':
    regtool = RegKeysTool()
    jout,OK = regtool.createRegistCode(100)
    datas = json.loads(jout)
    filename = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())  + '.txt'
    fpth = 'keys/' + filename
    outstr = ''
    for d in datas:
        outstr += d + '\n'

    f = open(fpth,'w')
    f.write(outstr)
    f.close()

    # keys = regtool.createRegistCode()
    # print(keys)
    # noregs = regtool.getNoAllRegCode()
    # print(noregs,len(noregs))
    # isOK  = regtool.addHardMsgToRegDB('06EpuPeppyQpwx4zXZryvHbm',{'cpu':182923})
    # noregs = regtool.getNoAllRegCode()
    # print(isOK,len(noregs))
    # print(regtool.db.allKeys())
    # print(len(noregs))
    # print(len(noregs))
    # regdata = regtool.getRegCodeData('06EpuPeppyQpwx4zXZryvHbm')
    # print(regdata)

# # 生成rsa密钥
# $ openssl genrsa -des3 -out server.key 2048
# # 去除掉密钥文件保护密码
# $ openssl rsa -in server.key -out server.key
# # 生成ca对应的csr文件
# $ openssl req -new -key server.key -out server.csr
# # 自签名
# $ openssl x509 -req -days 2048 -in server.csr -signkey server.key -out server.crt
# $ cat server.crt server.key > server.pem
