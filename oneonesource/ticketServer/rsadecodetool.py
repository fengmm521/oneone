#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-07 09:28:00
# @Link    : http://fengmm521.blog.163.com
# @Version : $Id$
#这里使用pycrypto‎库
#按照方法:easy_install pycrypto‎
 
import os,sys
import base64
import requests

# from Crypto import Random
# from Crypto.Hash import SHA
# from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
# from Crypto.PublicKey import RSA
import rsa

# https://www.cnblogs.com/hhh5460/p/5243410.html

class prpcrypt():
    def __init__(self,gkeyPth = 'rsakey'):
        self.gkeyPth = gkeyPth     #本地密钥保存地址
        
        self.gprivate_pem = None
        self.gpublic_pem = None
        self.readGhostKeyFromFile()
        if self.gprivate_pem == None or self.gpublic_pem == None:
            print('rsa key load erro')

    def readGhostKeyFromFile(self):
        pripth = self.gkeyPth + '/rsa_1024_priv.pem'
        if os.path.exists(pripth) and os.path.exists(pubpth):
            f = open(pripth,'r')
            if sys.version_info > (3,0):
                self.gprivate_pem = rsa.PrivateKey.load_pkcs1(f.read().encode())
            else:
                self.gprivate_pem = rsa.PrivateKey.load_pkcs1(f.read())
            f.close()
        else:
            print('本地RSA密钥文件不存在，可以文件丢失，请重新生成...')

    #使用本地私钥解密消息
    def decryptWithGhostPriKey(self,msg,isBase64In = False):
        dmsg = msg
        if isBase64In:
            dmsg = base64.b64decode(msg)
        text = rsa.decrypt(dmsg, self.gprivate_pem)
        return text

    def enbase64(self,msg):
        dmsg = base64.b64encode(msg)
        return dmsg
    def debase64(self,msg):
        dmsg = base64.b64decode(msg)
        return dmsg
    #使用本地私钥签名消息
    def signWithGhostPriKey(self,msg):
        tmpmsg = msg
        if sys.version_info > (3,0):
            tmpmsg = msg.encode()
        signature = rsa.sign(tmpmsg, self.gprivate_pem, 'SHA-1')
        return signature

if __name__ == '__main__':
    pc = prpcrypt(gkeyPth = '.')
    print('key create end')

    # msg = 'abcdefg---001'
    # pmsg = pc.encryptWithGhostPubKey(msg)
    # omsg = pc.decryptWithGhostPriKey(pmsg)

    # smsg = pc.signWithGhostPriKey(msg)
    # b64msg = pc.enbase64(msg)
    # vmsg = pc.verifyWithGhostPubKey(b64msg, smsg)

    # print('msg--->',msg)
    # print('pmsg-->',pmsg)
    # print('omsg-->',omsg)
    # print('smg-->',smsg)
    # print('vmsg-->',vmsg)
