#!/bin/bash
export PATH=/usr/local/bin:/usr/bin:$PATH
CUR_PATH=`pwd`
basepath=$(cd `dirname $0`; pwd)
echo $basepath
echo $CUR_PATH
#更新版本所要操作的步骤
#生成mac的服务器端
cd $basepath
cd ..
if [[ $1 ]]; then
    echo "开始生成mac服务器端:"
    if [[ -d "v"${1}/release-mac/server ]]; then
        rm -rf "v"${1}/release-mac/server
    fi
    mkdir "v"${1}/release-mac/server

    #复制可执行二进制文件
    cp "v${1}/OneLife/server/OneLifeServer" "v${1}/release-mac/server/"

    #复制资源文件
    cp -r v${1}/OneLifeData7/categories "v${1}/release-mac/server/"
    cp -r v${1}/OneLifeData7/objects "v${1}/release-mac/server/"
    cp -r v${1}/OneLifeData7/transitions "v${1}/release-mac/server/"
    cp v${1}/OneLifeData7/dataVersionNumber.txt "v${1}/release-mac/server/"

    #复制配置文件
    cp -r "v${1}/OneLife/server/settings" "v${1}/release-mac/server/"

    echo $1 > v${1}/release-mac/server/serverCodeVersionNumber.txt

    echo 0 > v${1}/release-mac/server/settings/requireTicketServerCheck.ini
    echo 1 > v${1}/release-mac/server/settings/forceEveLocation.ini

    echo "开始生成mac服务器端完成"
else
    echo "请输入onelife编译版本号"
fi

