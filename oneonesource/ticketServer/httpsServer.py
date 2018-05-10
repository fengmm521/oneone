#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-07 09:28:00
# @Link    : http://fengmm521.blog.163.com
# @Version : $Id$
#https服务器
import os
import ssl
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading
import cgi
import time
import posixpath
import urllib
import sys
import shutil
import mimetypes
import json
import base64
import hashlib
import datetime

import rsadecodetool
import hmactool

import zlib

# import Cookie

import servertool

reload(sys)  
sys.setdefaultencoding('utf8')  


configdic = {}

users = {}

usercookies = {}    #usercookies

def updateUser():
    global configdic
    global users
    global usercookies
    f = open('./config.txt','r')
    jstr = f.read()
    f.close()
    configdic = json.loads(jstr)

updateUser()


serverstattool = servertool.ServerUser(configdic['logdir'])

rsatool = rsadecodetool.prpcrypt()

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

nowPth = os.path.split(os.getcwd())[1]
curdir = '.'

import socket
hostname = socket.gethostname()
selfip = socket.gethostbyname(hostname)




setLastIP = selfip



print 'selfIP:',selfip
print 'setLastIP:',setLastIP




def serUserCooke(email,pwd):
    tmpcookie = hashlib.md5(email + pwd).hexdigest()
    usercookies[tmpcookie] = True
    return tmpcookie

allUserData = {}
#服务器初始化用户数据
def initAllUserData():
    global allUserData
    allUserData = {}
    f = open('db/user.txt','r')
    lines = f.readlines()
    f.close()
    for l in lines:
        if len(l) < 20:
            continue
        tmpl = l.replace('\n','')
        dats = tmpl.split(',')
        allUserData[dats[0]] = {}
        #email@test.com,gametest77889900,name,qq,yaoqingcode,注册ip地址,注册日期,购买次数
        allUserData[dats[0]]['email'] = dats[0]
        allUserData[dats[0]]['pwd'] = dats[1]
        allUserData[dats[0]]['name'] = dats[2]
        allUserData[dats[0]]['qq'] = dats[3]
        allUserData[dats[0]]['code'] = dats[4]
        allUserData[dats[0]]['ip'] = dats[5]
        allUserData[dats[0]]['date'] = dats[6]
        allUserData[dats[0]]['buy'] = int(dats[7])
        serUserCooke(dats[0], dats[1])



initAllUserData()


#获取cookie过期时间
def getNewCookieExpTime():
    expiration = datetime.datetime.now() + datetime.timedelta(days=30)  
    return expiration



def createServerListHtml():
    count,minxinguser,userdatas = serverstattool.getServerStat()
    try:
        userqq = allUserData[minxinguser]['qq']
        username = allUserData[minxinguser]['name']
        outname = username + '(' + userqq + ')'
    except Exception as e:
        outname = minxinguser
    
    f = open('html/slistframe.html','r')
    outhtml = f.read()
    f.close()

    p1 = outhtml.find('$1')
    p2 = outhtml.find('$2')
    fronthtml = outhtml[:p1]
    endhtml = outhtml[p2+2:]

    mhtml = '''
    <tr>
        <td valign="middle" align="center" width="30" height="40" overflow="hidden" display="block" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            1
        </td>
        <td valign="middle" align="center" width="40" height="40" overflow="hidden" display="block" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            132871641
        </td>
        <td width="40" align="center" height="40" align="center" valign="middle" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            野醋栗
        </td>
        <td valign="middle" width="60" height="40" overflow="hidden" display="block" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            server1.woodcol.com
        </td>
        <td valign="middle" align="center" width="40" height="40" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            %s/200
        </td>
        <td valign="middle" align="center" width="50" height="40" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            %s
        </td>
        <td valign="middle" align="center" width="40" height="40" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            <form action='./userlist?serverid=1' id="userform" method='get'>
            <input class="submit" type='submit' value='查看今日玩家战况' onclick="gotouser()"/>
            </form>
        </td>
  </tr>

    '''%(str(count),outname)

    tochtml =  fronthtml + mhtml + endhtml

    return tochtml

def createUserListHtml():
    count,minxinguser,userdatas = serverstattool.getServerStat()
    f = open('html/ulistframe.html','r')
    outhtml = f.read()
    f.close()

    p1 = outhtml.find('$1')
    p2 = outhtml.find('$2')
    fronthtml = outhtml[:p1]
    endhtml = outhtml[p2+2:]

    mhtml = ''
    userdatas.reverse()
    for u in userdatas:
        #[account,isB,tstr,age,fposion,playerstat,countplayer,parent]
        try:
            userqq = allUserData[u[0]]['qq']
            username = allUserData[u[0]]['name']
            d1 = username + '(' + userqq + ')'
        except Exception as e:
            d1 = u[0]
        
        d2 = '出生'
        if u[1] == 'D':
            d2 = '死亡'
        d3 = u[2].split('_')[1]
        d4 = u[3]
        d5 = u[4]
        d6 = '出生'
        if u[1] == 'D':
            d6 = u[5]

        d7 = ''
        if u[7] != 'noParent':
            try:
                userqq7 = allUserData[u[7]]['qq']
                username7 = allUserData[u[7]]['name']
                d7 = username7 + '(' + userqq7 + ')'
            except Exception as e:
                d7 = u[7]
            
        else:
            d7 = '夏娃'
        d8 = u[6]
        mhtml += '''
        <tr>
        <td valign="middle" align="center" width="40" height="40" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            %s
        </td>
        <td valign="middle" align="center" width="30" height="40" overflow="hidden" display="block" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            %s
        </td>
        <td valign="middle" align="center" width="30" height="40" overflow="hidden" display="block" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            %s
        </td>
        <td width="30" align="center" height="40" align="center" valign="middle" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            %s
        </td>
        <td align="center" valign="middle" width="40" height="40" overflow="hidden" display="block" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            %s
        </td>
        <td valign="middle" align="center" width="40" height="40" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            %s
        </td>
        <td valign="middle" align="center" width="60" height="40" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            %s
        </td>
        <td valign="middle" align="center" width="60" height="40" style="word-break: break-all; word-wrap: 14; text-overflow: ellipsis; overflow-y: hidden; overflow-x: hidden; font-size: 14px;">
            %s
        </td>
        
  </tr>
        '''%(d1,d2,d3,d4,d5,d6,d7,d8)

    tochtml =  fronthtml + mhtml + endhtml
    return tochtml

#保存新用户帐号
def saveNewUserData(email,pstr):
    global allUserData
    if email in allUserData:
        allUserData[email]['buy'] += 1
        cmd = 'cp db/user.txt db/userback.txt'
        os.system(cmd)
        outstr = ''
        #email@test.com,gametest77889900,name,qq,yaoqingcode,注册ip地址,注册日期
        tmpstr = pstr.replace('\n','')
        pdatas = tmpstr.split(',')
        for k in allUserData.keys():
            if k == email:
                outstr += pdatas[0] + ',' + pdatas[1] + ',' + pdatas[2] + ',' + pdatas[3] + ',' + pdatas[4] + ',' + pdatas[5]+ ',' + pdatas[6] + ',' + str(allUserData[k]['buy'])
                serUserCooke(pdatas[0], pdatas[1])
            else:
                outstr += k + ',' + allUserData[k]['pwd'] + ',' + allUserData[k]['name'] + ',' + allUserData[k]['qq'] + ',' + allUserData[k]['code'] + ',' + allUserData[k]['ip'] + ',' + allUserData[k]['date'] + ',' + str(allUserData[k]['buy'])
            outstr += '\n'
        f = open('db/user.txt','w')
        f.write(outstr)
        f.close()

    else:
        f = open('db/user.txt','a+')
        f.write(pstr)
        f.close()
        tmpstr = pstr.replace('\n','')
        dats = tmpstr.split(',')
        allUserData[dats[0]] = {}
        allUserData[dats[0]]['email'] = dats[0]
        allUserData[dats[0]]['pwd'] = dats[1]
        allUserData[dats[0]]['name'] = dats[2]
        allUserData[dats[0]]['qq'] = dats[3]
        allUserData[dats[0]]['code'] = dats[4]
        allUserData[dats[0]]['ip'] = dats[5]
        allUserData[dats[0]]['date'] = dats[6]
        allUserData[dats[0]]['buy'] = int(dats[7])
        serUserCooke(dats[0], dats[1])

def saveNewActionCode(pcode):
    f = open('db/actioncode.txt','a+')
    f.write(pcode + '\n')
    f.close()

#验证邀请码是否存在，或者是否已被使用
def checkCode(code):
    newcodepth = 'db/newcode.txt'
    f = open(newcodepth,'r')
    lines = f.readlines()
    f.close()

    isHeave = False
    outstr = ''
    for l in lines:
        tmpl = l.replace('\n','')
        if tmpl == code:
            isHeave = True
            saveNewActionCode(code)
        else:
            outstr += l
    if isHeave:
        f = open(newcodepth,'w')
        f.write(outstr)
        f.close()
    return isHeave

#查看用户帐号和密码是否正确，用以登陆网页
def checkUserLogin(email,pwd):
    if allUserData[email]['pwd'] == pwd:
        return True
    else:
        return False

def getUserPwd(email):
    return allUserData[email]['pwd']

def getServerUserListHtml(serverid):
    pass


class myHandler(BaseHTTPRequestHandler):
    
    #刷新数据
    #http://sell1.woodcol.com:8902/ticketserver?action=check_ticket_hash&email=test%40test.com&hash_value=1cd5e064500c686a76d923b646437e06f693eaef&string_to_hash=2
    #text/html; charset=UTF-8
    def chickTicket(self,logindat):
        print(logindat)
        # self.sendMsg('login')
        # {'pwd': 'aaa', 'usename': 'aaa'}
        isPass = False
        pemail = urllib.unquote(logindat['email'])      #邮箱
        phashvalue = logindat['hash_value']             #字符串hash后的结果
        pstringToHash = logindat['string_to_hash']      #使用hash的字符串
        paction = logindat['action']                    #check_ticket_hash
        if paction != 'check_ticket_hash':
            print('paction=%s'%(paction))
            self.sendEmptyMsg()
            return
        sk = getUserPwd(pemail)
        tmphash = hmactool.get_authorization(sk, pstringToHash)
        if tmphash == phashvalue:
            self.sendTxtMsg("VALID")
        else:
            self.sendTxtMsg("INVALID")

    def regGame(self,cdataobj):
        pcode = urllib.unquote(cdataobj['cod'])
        pcode = rsatool.decryptWithGhostPriKey(pcode)
        if checkCode(pcode):
            pemail = urllib.unquote(cdataobj['mail'])
            pemail = rsatool.decryptWithGhostPriKey(pemail)
            ppwd = urllib.unquote(cdataobj['pwd'])
            ppwd = rsatool.decryptWithGhostPriKey(ppwd)
            
            pname = cdataobj['usename']
            pqq = cdataobj['qq']

            print(pemail,ppwd,pcode,pname)
            #email@test.com,gametest77889900,name,qq,yaoqingcode,注册ip地址,注册日期
            outstr = pemail + ',' + ppwd + ',' + pname + ',' + pqq + ',' + pcode + ',' + self.client_address[0] + ',' +time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) + ',' + '1\n'
            saveNewUserData(pemail,outstr)
            self.sendHtmlStr('注册成功，游戏客户端在群共享中，请从QQ群(%s)中下载。'%(configdic['qun']))
        else:
            self.sendHtmlStr('输入的邀请码错误，请确认你输入了正确的邀请码.')

    def saveUserLoginData(self,email):
        userlogindir = 'db/userlogin/'
        tpth = userlogindir + email + '.txt'
        savestr = self.client_address[0] + ',' +time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) + '\n'
        f = open(tpth,'a+')
        f.write(savestr)
        f.close()

    def userLogin(self,cdataobj):
        pemail = urllib.unquote(cdataobj['mail'])
        print(pemail)
        pemail = rsatool.decryptWithGhostPriKey(pemail)
        print('---')
        print(pemail)
        ppwd = urllib.unquote(cdataobj['pwd'])
        ppwd = rsatool.decryptWithGhostPriKey(ppwd)
        print(pemail,ppwd)
        if checkUserLogin(pemail, ppwd):
            self.saveUserLoginData(pemail)
            htmlpth = 'html/list.html'
            sessionstr = serUserCooke(pemail, ppwd)
            cookiestr = "sessionID=%s"%(sessionstr)
            self.sendHtml(htmlpth,cookiestr)
        else:
            self.sendHtmlStr('登陆失败，用户名或者密码错误.')

    def checkCookie(self,cookiestr):
        print(cookiestr)
        if cookiestr:
            cs = cookiestr.split(';')
            for c in cs:
                tmpss = c.split('=')[1]
                if tmpss in usercookies and usercookies[tmpss]:
                    return True
        return False
    def do_GET(self):  
    	print('clientIP-->',self.client_address[0])
        print('clienturl-->',self.path)
        cookiestr = self.headers.getheader('Cookie');
        print('clientcookie---->',cookiestr)
        if self.path=="/":  
            if self.checkCookie(cookiestr):
                self.path="/list.html"
            else:
                self.path="/index.html"  
        if self.path[1:13] == "ticketserver": 
            #http://sell1.woodcol.com:8902/ticketserver?action=check_ticket_hash&email=test%40test.com&hash_value=1cd5e064500c686a76d923b646437e06f693eaef&string_to_hash=2
            tcikobj = self.path.split('?')[1]
            tmpobj = tcikobj.split('&')
            outdic = {}
            for d in tmpobj:
                tmpx = d.split('=')
                outdic[tmpx[0]] = tmpx[1]
            self.chickTicket(outdic)
        else:
            try:  
                #根据请求的文件扩展名，设置正确的mime类型  
                print(self.path[1:9])
                if self.path[-1] == '?':
                    self.path = self.path[:-1]
                elif self.path.find('?') != -1:
                    # ./userlist?serverid=1
                    tmps = self.path.split('?')[1]
                    serverid = tmps.split('=')[1]
                    if serverid == '1':
                        self.path = "/user.html"
                    else:
                        self.path = "/user.html"

                if self.path.endswith(".html"):  
                    if self.checkCookie(cookiestr):
                        if self.path[-15:] == 'slistframe.html':
                            htmlstr = createServerListHtml()
                            self.sendHtmlStr(htmlstr)
                        elif self.path[-15:] == 'ulistframe.html':
                            htmlstr = createUserListHtml()
                            self.sendHtmlStr(htmlstr)
                        else:
                            fpth = curdir + os.sep + 'html' + os.sep + self.path
                            self.sendHtml(fpth)
                    elif self.path[1:9] == 'reg.html':
                        print('reg.html run')
                        fpth = curdir + os.sep + 'html' + os.sep + 'reg.html'
                        self.sendHtml(fpth)
                    else:
                        fpth = curdir + os.sep + 'html' + os.sep + 'index.html'
                        self.sendHtml(fpth)
                    return
                elif self.path[1:4] == 'img':
                    fpth = curdir + self.path
                    self.sendImage(fpth)
                elif self.path[1:4] == 'bin':
                    fpth = curdir + self.path
                    self.sendJsFile(fpth)
                elif self.path[1:6] == 'login':#客户端登录
                    print('login--->',self.path)
                    return 'login'
                elif self.path[1:6] == 'ooreg': #用户注册
                    print('ooreg---->',self.path)
                    return 'ooreg'
                else:
                    time.sleep(3)
                    self.sendEmptyMsg()
                return  
            except IOError:  
                self.send_error(404,'File Not Found: %s' % self.path)  

    def sendHtmlStr(self,htmlstr):
        mimetype='text/html;charset=UTF-8'  
        self.send_response(200)  
        self.send_header('Content-type',mimetype)  
        self.end_headers()
        self.wfile.write(htmlstr)  

    def sendImage(self,imgpth):
        f = open(imgpth, 'rb') 
        mimetype='image/*'  
        self.send_response(200)  
        self.send_header('Content-type',mimetype)  
        self.end_headers()
        self.wfile.write(f.read())  
        f.close()  

    def sendJsFile(self,jsfpth):
        f = open(jsfpth,'r')
        mimetype='application/javascript'
        self.send_response(200)
        self.send_header('Content-type',mimetype)
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
    
    def sendHtml(self,fpth,pcookie = None):
        f = open(fpth, 'rb') 
        mimetype='text/html'  
        self.send_response(200)  
        if pcookie:
            print(pcookie)
            self.send_header("Set-Cookie",pcookie)
        self.send_header('Content-type',mimetype)  
        self.end_headers()
        self.wfile.write(f.read())  
        f.close()  

    def decodePostData(self,strdata):
        tmps = strdata.split('&')
        out = {}
        for d in tmps:
            objtmp = d.split('=')
            out[objtmp[0]] = objtmp[1]
        return out

    def do_POST(self):

        reqtype = self.do_GET()
        # try:
        if True:
            length = self.headers.getheader('content-length');
            nbytes = int(length)
            data = self.rfile.read(nbytes)
            print(data)
            msgobj = self.decodePostData(data)
            if reqtype == 'ooreg':  
                self.regGame(msgobj)
            elif reqtype == 'login':
                self.userLogin(msgobj)
            elif self.path == "/index.html":
                return
            else:
                self.sendEmptyMsg()

        # except Exception as e:
            # self.send_error(404,'File Not Found: %s' % self.path)  
    def sendEmptyMsg(self):
        self.send_response(200)
        self.send_header("Content-type", 'text/json; encoding=utf-8')
        self.send_header("Content-Length", str(''))
        self.end_headers()
        self.wfile.write('')



    def sendTxtMsg(self,msg,isCompress = False):
        outstr = ''
        if isCompress:
            demsg = self._compress(msg)
            outstr = base64.b64encode(demsg)
        else:
            outstr = msg
        self.send_response(200)
        self.send_header("Content-type", 'text/json;charset=utf-8')
        self.send_header("Content-Length", str(len(outstr)))
        self.end_headers()
        self.wfile.write(outstr)

    #校验消息真实性
    def verifyMsg(self,reqdict):
        tokenver = []
        tokenver.append('tokenxxx')
        tokenver.append(reqdict['nonce'])
        tokenver.append(reqdict['timestamp'])
        tokenver.sort()
        tmpstr = tokenver[0] + tokenver[1] + tokenver[2]
        sha1str = hashlib.sha1(tmpstr).hexdigest()
        if sha1str == reqdict['signature']:
            return True
        else:
            return False

    def _compress(self,msg):
        dat = zlib.compress(msg, zlib.Z_BEST_COMPRESSION)
        # print('ziplen-co-->',len(msg),len(dat))
        return dat
    def _decompress(self,dat):
        msg = zlib.decompress(dat)
        # print('ziplen-de-->',len(dat),len(msg))
        return msg


    def do_HEAD(self):
        """Serve a HEAD request."""
        print('do_HEAD')
        f = self.send_head()
        if f:
            f.close()

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write('''<form action="" enctype="multipart/form-data" method="post">\n
                    <input name="file" type="file" />
                    <input value="upload" type="submit" />
                </form>''')
        f.write("<hr>\n<ul>\n")
        for name in list:
            if name.startswith('.'):
                continue
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write('<li><a href="%s">%s</a>\n'
                    % (urllib.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        encoding = sys.getfilesystemencoding()
        self.send_header("Content-type", "text/html; charset=%s" % encoding)
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)

    def log_error(self, format, *args):
        """Log an error.

        Display error message in red color.
        """

        format = '\033[0;31m' + format + '\033[0m'
        self.log_message(format, *args)

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


tmpIp = configdic['ip']
tmpPort = configdic['port']

serverAddr = (selfip,tmpPort)

if selfip[0:2] != '19':
    serverAddr = (tmpIp,tmpPort)

def runHttpServer(ptemp):

    server = ThreadedHTTPServer(serverAddr, myHandler)
    print('https server is running....')
    print('Starting server, use <Ctrl-C> to stop')
    print(serverAddr)
    
    # server.socket = ssl.wrap_socket (server.socket, certfile='./keys/server.pem', server_side=True)
    server.serve_forever()
def startServer():

    thr = threading.Thread(target=runHttpServer,args=(None,))
    thr.setDaemon(True)
    thr.start()

    

if __name__ == '__main__':
    # server = ThreadedHTTPServer(serverAddr, myHandler)
    # print 'https server is running....'
    # print 'Starting server, use <Ctrl-C> to stop'
    # server.socket = ssl.wrap_socket (server.socket, certfile='server.pem', server_side=True)
    # server.serve_forever()

    startServer()
    while True:
        time.sleep(600)


# # 生成rsa密钥
# $ openssl genrsa -des3 -out server.key 2048
# # 去除掉密钥文件保护密码
# $ openssl rsa -in server.key -out server.key
# # 生成ca对应的csr文件
# $ openssl req -new -key server.key -out server.csr
# # 自签名
# $ openssl x509 -req -days 2048 -in server.csr -signkey server.key -out server.crt
# $ cat server.crt server.key > server.pem
