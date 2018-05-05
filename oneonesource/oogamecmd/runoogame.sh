#!/bin/sh


cd /root/game/OneLife/server

export PATH=/usr/bin/:/usr/local/bin:/bin:
DATE=`date "+%Y-%m-%d %H:%M:%S"`
echo $DATE


LOG=`nohup /root/game/OneLife/server/OneLifeServer > log.txt 2>&1 & echo $!`
echo $LOG
OUTSTR=$DATE"\n"$LOG
echo $OUTSTR > psid.txt
