#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-12 01:04:18
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os,sys
import shutil
import json
import codecs
import chardet
import urllib2

# http://guide.onehouronelife.cn/static/objects.json

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

def cmp(a,b):
    return ((a>b)-(a<b))

#获取父目录
def GetParentPath(strPath):
    if not strPath:
        return None;
    lsPath = os.path.split(strPath);
    if lsPath[1]:
        return lsPath[0];
    lsPath = os.path.split(lsPath[0]);
    return lsPath[0];

#获取目录下的所有类型文件
def getAllExtFile(pth,fromatx = ".erl"):
    jsondir = pth
    jsonfilelist = []
    for root, _dirs, files in os.walk(jsondir):
        for filex in files:          
            #print filex
            name,text = os.path.splitext(filex)
            if cmp(text,fromatx) == 0:
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
            elif fromatx == ".*" :
                jsonArr = []
                rootdir = pth
                dirx = root[len(rootdir):]
                pathName = dirx +os.sep + filex
                jsonArr.append(pathName)
                (newPath,_name) = os.path.split(pathName)
                jsonArr.append(newPath)
                jsonArr.append(name)
                jsonfilelist.append(jsonArr)
    return jsonfilelist


def getAllObjPth(vpth):
    objspth = vpth + os.sep + 'OneLifeData7' + os.sep + 'objects'

    alltxtpths = getAllExtFile(objspth,'.txt')
    return alltxtpths,objspth

def hanhuaObjs(vpth):
    hanhuapth = vpth + os.sep +'hanhua'

    if not os.path.exists(hanhuapth):
        os.mkdir(hanhuapth)
    else:
        shutil.rmtree(hanhuapth)
        os.mkdir(hanhuapth)

    windowsPth = hanhuapth + os.sep + 'windows'
    macpth = hanhuapth + os.sep + 'macos'

    os.mkdir(windowsPth)
    os.mkdir(macpth)

    os.mkdir(windowsPth + os.sep + 'objects')
    os.mkdir(macpth + os.sep + 'objects')

    hjsonpth = cur_file_dir() + os.sep + 'oneonesource' + os.sep + 'zh/objects.json'

    f = codecs.open(hjsonpth,'r','utf8')
    jstr = f.read()
    f.close()
    hjsonobj = json.loads(jstr)
    ids = hjsonobj['ids']
    names = hjsonobj['names']
    objs = {}
    for i, val in enumerate(ids):
        objs[val] = names[i]

    return objs


def changeTxtForMacOS(vpth,opth,idstr,zhstr):
    macospth = vpth + os.sep +'hanhua' + os.sep + 'macos' + os.sep + 'objects' + os.sep + idstr + '.txt'
    f = codecs.open(opth,'r','utf8')
    lines = f.readlines()
    f.close()
    lines[1] = zhstr + '\n'
    savestr = ''.join(lines)
    f = codecs.open(macospth,'w','utf8')
    f.write(savestr)
    f.close()

def changeTxtForWindows(vpth,opth,idstr,zhstr):
    macospth = vpth + os.sep +'hanhua' + os.sep + 'windows' + os.sep + 'objects' + os.sep + idstr + '.txt'
    f = codecs.open(opth,'r','utf8')
    lines = f.readlines()
    f.close()
    lines[1] = zhstr + '\n'
    savestr = ''.join(lines)
    f = codecs.open(macospth,'w','utf_8_sig')
    f.write(savestr)
    f.close()

def conventStrTOUtf8(oldstr):
    try:
        nstr = oldstr.encode("utf-8")
        return nstr
    except Exception as e:
        print 'nstr do not encode utf-8'
    cnstrtype = chardet.detect(oldstr)['encoding']
    utf8str =  oldstr.decode(cnstrtype).encode('utf-8')
    return utf8str

def getUrl(purl):
    try:
        req = urllib2.Request(purl)
        req.add_header('User-agent', 'Mozilla 5.10')
        res = urllib2.urlopen(req)
        html = conventStrTOUtf8(res.read())
        return html
    except Exception, e:
        print e
    return None

def getJsonFileFromServer():
    jsonurl = 'http://guide.onehouronelife.cn/static/objects.json'
    jstr = getUrl(jsonurl)
    jdic = json.loads(jstr)
    print(len(jdic))
    if len(jdic) > 9:
        hjsonpth = cur_file_dir() + os.sep + 'oneonesource' + os.sep + 'zh/objects.json'
        f = open(hjsonpth,'w')
        f.write(jstr)
        f.close()
    else:
        print('get json objects erro')
def main(vpth):
    getJsonFileFromServer()
    objs = hanhuaObjs(vpth)
    txtpth,objspth = getAllObjPth(vpth)
    # print(txtpth[0])
    for i,v in enumerate(txtpth):
        if objs.has_key(v[2]):
            opth = objspth + v[0]
            print(opth)
            changeTxtForMacOS(vpth,opth,v[2],objs[v[2]])
            # changeTxtForWindows(vpth,opth,v[2],objs[v[2]])
def test():
    getJsonFileFromServer()
#测试

# if __name__ == '__main__':
#     test()
if __name__ == '__main__':
    args = sys.argv
    fpth = ''
    if len(args) == 2 :
        if os.path.exists(args[1]):
            fpth = args[1]
            main(fpth)
        else:
            print "1请加上要汉化的游戏版本路径"
    else:
        print "2请加上要汉化的游戏版本路径"
    
