#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys
import time
import dbTool
import json

from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding( "utf-8" )

def conventDBToJson():
    dbpth = 'db' + os.sep + 'data.db'
    if not os.path.exists(dbpth):
        outstr = '数据库不存在:%s'%(dbpth)
        print(outstr.decode())
        return
    db = dbTool.DBMObj(dbpth)
    dicdat = db.getDBDatas()
    jstr = json.dumps(dicdat)
    if not os.path.exists('jsonout'):
        os.mkdir('jsonout')
    f = open('jsonout' + os.sep + 'jsondb.json','w')
    f.write(jstr)
    f.close()

def main():
    conventDBToJson()

#测试
if __name__ == '__main__':
    main()




