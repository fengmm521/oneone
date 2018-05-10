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
    def __init__(self,gkeyPth = 'rsakey',isTest = False):
        self.gkeyPth = gkeyPth     #本地密钥保存地址
        
        self.gprivate_pem = None
        self.gpublic_pem = None
        self.readGhostKeyFromFile(isTest)
        if self.gprivate_pem == None or self.gpublic_pem == None:
            print('rsa key load erro')

    def readGhostKeyFromFile(self,isTest = False):
        pripth = self.gkeyPth + '/rsa_1024_priv.pem'
        print(pripth)
        if os.path.exists(pripth):
            f = open(pripth,'r')
            if sys.version_info > (3,0):
                self.gprivate_pem = rsa.PrivateKey.load_pkcs1(f.read().encode())
            else:
                self.gprivate_pem = rsa.PrivateKey.load_pkcs1(f.read())
            f.close()
            if isTest:
                f = open(self.gkeyPth + '/rsa_1024_pub.pem','r')
                print('-'*10)
                self.gpublic_pem = rsa.PublicKey.load_pkcs1_openssl_pem(f.read())
                f.close()
        else:
            print('本地RSA密钥文件不存在，可能文件丢失，请重新生成...')

    #使用本地公钥加密消息数据
    def encryptWithGhostPubKey(self,msg,isBase64Out = True):
        tmpmsg = msg
        if sys.version_info > (3,0):
            tmpmsg = msg.encode()
        if isBase64Out:
            cipher_text = base64.b64encode(rsa.encrypt(tmpmsg, self.gpublic_pem))
            return cipher_text
        else:
            dmsg = rsa.encrypt(tmpmsg, self.gpublic_pem)
            return dmsg
    #使用本地私钥解密消息
    def decryptWithGhostPriKey(self,msg,isBase64In = True):
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
    pc = prpcrypt(isTest = True)
    print('key create end')
    import urllib
    msg = 'mage'
    pmsg = pc.encryptWithGhostPubKey(msg)
    omsg = pc.decryptWithGhostPriKey(pmsg)

    turlmsg = urllib.quote(pmsg)
    print('turlmsg---->')
    print(turlmsg)
    bpmsg = base64.b64encode(pmsg)

    print('base64---->')
    print(bpmsg)
    urlmsg = urllib.quote(bpmsg)
    print('urlmsg---->')
    print(urlmsg)
    print(len(urlmsg))

    testurl = r'ZOCpThM5AY2B0%2BIv6rS4dSG3qXY6EVIX7CUljwZxkYsUEiy7ysuI9IinHBTIw6LCWwE2YtPPUw6LhV6nQfO0gx2EQM2V3cUMvA4kOKfTDDnR3mdlOnCNwTAhN8%2F%2Fl4IQ6KFwlpB0RXM%2BsXzZgh%2BWCg1TM%2FpF5Cy0h0L%2F2LosTqw%3D'

    durl = urllib.unquote(testurl)
    oomsg = pc.decryptWithGhostPriKey(durl)
    print('oomsg---->')
    print(oomsg)
    # smsg = pc.signWithGhostPriKey(msg)
    # b64msg = pc.enbase64(msg)
    # vmsg = pc.verifyWithGhostPubKey(b64msg, smsg)

    print('msg--->',msg)
    print('pmsg-->',pmsg)
    print('omsg-->',omsg)
    # print('smg-->',smsg)
    # print('vmsg-->',vmsg)
