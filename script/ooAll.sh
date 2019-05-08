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
cd ..
if [[ $3 ]]; then

   sh script/o1OneLife.sh  $1
   sh script/o2OneLifeData7.sh $1 $2
   sh script/o3MinorGems.sh $1 $3

#修改汉化部分代码
   python script/changeToCH.py $1

   #开始生成server的makefile
   cd "v"${1}/OneLife/server
   ./configure 2      #1.GNU/linux,2.MacOSX,3.win32 using MinGW
   make                 #开始编译服务器端

   #生成客户端makeFIle
   cd ..
   ./configure 2

   cd $basepath
   cd ..

   #修改makefile
   python script/changeMakeFile.py $1
   cd "v"${1}/OneLife/gameSource
   make   #开始编译客户端

   #编译地图编译器
   sh ./makeEditor.sh

else
    echo "请输入onelife，minorGems的要更新到的版本号"
fi



