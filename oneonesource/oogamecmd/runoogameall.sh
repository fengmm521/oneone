#!/bin/sh


export PATH=/usr/bin/:/usr/local/bin:/bin:
DATE=`date "+%Y-%m-%d %H:%M:%S"`
echo $DATE


LOG=`nohup python pythoncode/pswatchdog.py > log.txt 2>&1 & echo $!`
echo $LOG
OUTSTR=$DATE"\n"$LOG
echo $OUTSTR > psid.txt

