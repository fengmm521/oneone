#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-12 01:04:18
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os,sys
import shutil
import codecs

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
    objspth = vpth

    alltxtpths = getAllExtFile(objspth,'.txt')
    return alltxtpths,objspth

def hanhuaObjs(oldfile,newfile):
    f = codecs.open(oldfile,'r','utf8')
    utfstr = f.read()
    f.close()

    outansestr = utfstr.encode('mbcs')

    f = open(newfile,'wb')
    f.write(outansestr)
    f.close()

def createObjectsDir():
    if os.path.exists('objects'):
        shutil.rmtree('objects')
    os.mkdir('objects')
def main():
    vpth = 'objects_utf8'
    txtpth,objspth = getAllObjPth(vpth)
    # print(txtpth[0])
    createObjectsDir()
    for i,v in enumerate(txtpth):
        oldfile = objspth + v[0]
        newfile = 'objects' + v[0]
        hanhuaObjs(oldfile, newfile)

#测试
if __name__ == '__main__':
    main()
    # args = sys.argv
    # fpth = ''
    # if len(args) == 2 :
    #     if os.path.exists(args[1]):
    #         fpth = args[1]
    #         main(fpth)
    #     else:
    #         print "1请加上要汉化的游戏版本路径"
    # else:
    #     print "2请加上要汉化的游戏版本路径"
    
