#!/bin/bash
export PATH=/usr/local/bin/:$PATH
CUR_PATH=`pwd`
basepath=$(cd `dirname $0`; pwd)
echo $basepath
echo $CUR_PATH
#更新版本所要操作的步骤
#1.选将三个游戏相关的git项目切换回master主分支
#2.再分别更新主分支到最新版
#3.再分别将三个git切换到相应的tag版本,所以在启动脚本时需要输入onelife，onelifeData7，minorGems所要切换的版本号
#4.再将相应的游戏目录复制到onelife版本为名称的新目录下
#####上边的四步使用shell脚本来完成
#5.对代码相应部分进行汉化和修改
#6.开始编译Mac版的新客户端和服务器端，并修改相应的设置文件为单机可运行版
#7.编译完成后，先运行服务器端，等5秒后，自动运行客户端
cd $basepath

if [[ $3 ]]; then
    if [[ -d "v"${1}/release-mac ]]; then
        rm -rf "v"${1}/release-mac
      fi
    mkdir "v"${1}/release-mac
    sh script/ooAll.sh $1 $2 $3
    sh script/makeMacServer.sh $1
    sh script/makeMacApp.sh $1
    sh script/makeMacEditorApp.sh $1
else
    echo "请输入onelife，oneLifeData7,minorGems的要更新到的版本号"
fi



