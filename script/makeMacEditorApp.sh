#!/bin/bash
export PATH=/usr/local/bin:/usr/bin:$PATH
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
if [[ $1 ]]; then
    if [[ -d "v"${1} ]]; then
      if [[ -d "v"${1}/release-mac/Editor ]]; then
        rm -rf "v"${1}/release-mac/Editor
      fi
      mkdir "v"${1}/release-mac/Editor
      cp -r oneonesource/zh/mac_zh/EditOneLife.app "v${1}/release-mac/Editor/EditOneLife_v${1}.app"
      cp -f "v${1}/OneLife/gameSource/EditOneLife" "v${1}/release-mac/Editor/EditOneLife_v${1}.app/Contents/MacOS/EditOneLife"


      #修改OneLife可执行文件的动太库
      cp -r v${1}/release-mac/client/OneLife_v${1}.app/Contents/Frameworks/SDL.framework v${1}/release-mac/Editor/EditOneLife_v${1}.app/Contents/Frameworks/
      cp -f v${1}/release-mac/client/OneLife_v${1}.app/Contents/Frameworks/libpng16.16.dylib v${1}/release-mac/Editor/EditOneLife_v${1}.app/Contents/Frameworks/libpng16.16.dylib
      otool -L v${1}/release-mac/Editor/EditOneLife_v${1}.app/Contents/MacOS/EditOneLife
      install_name_tool -change /usr/local/opt/freetype/lib/libfreetype.6.dylib @executable_path/../Frameworks/libfreetype.6.dylib v${1}/release-mac/Editor/EditOneLife_v${1}.app/Contents/MacOS/EditOneLife
      cp -f v${1}/release-mac/client/OneLife_v${1}.app/Contents/Frameworks/libfreetype.6.dylib v${1}/release-mac/Editor/EditOneLife_v${1}.app/Contents/Frameworks/libfreetype.6.dylib
      otool -L v${1}/release-mac/Editor/EditOneLife_v${1}.app/Contents/MacOS/EditOneLife

    else
      echo "没有找到v${1}目录，相应版本的代码目录不存在"
    fi
else
    echo "请输入onelife编译版本号，和dataversion版本号"
fi

