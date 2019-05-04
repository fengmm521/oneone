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
if [[ $2 ]]; then
    if [[ -d "v"${1} ]]; then
        if [[ -d "v"${1}/OneLifeData7 ]]; then
            rm -r "v"${1}/OneLifeData7
        fi
    fi
    mkdir "v"${1}/OneLifeData7
    
    #OneLifeData7项目
    cd ../OneLifeData7
    git checkout master     #切换到主分支
    git pull                #拉取最新代码
    git checkout "OneLife_v"${2}
    cp -r `ls | grep -v ".git" | xargs` "../oneone/v${1}/OneLifeData7"
    git checkout -b "v"${2}

else
    echo "请输入onelife更新到的版本号和onelifeData7更新到的版本号"
fi



