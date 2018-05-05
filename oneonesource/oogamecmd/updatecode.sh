#!/bin/sh

cd /root/checkout/OneLife
latestOneLifeVersion=`git for-each-ref --sort=-creatordate --format '%(refname:short)' --count=1 refs/tags | sed -e 's/OneLife_v//'`
git checkout -q OneLife_v$latestOneLifeVersion

echo "latest OneLife version = "${latestOneLifeVersion}

cd /root/checkout/OneLifeData7
git fetch --tags
latestOneLifeData7Version=`git for-each-ref --sort=-creatordate --format '%(refname:short)' --count=1 refs/tags | sed -e 's/OneLife_v//'`
git checkout -q OneLife_v$latestOneLifeData7Version

echo "latest OneLifeData7 version = "${latestOneLifeData7Version}


cd /root/checkout/minorGems
git fetch --tags
latestMinorGemsVersion=`git for-each-ref --sort=-creatordate --format '%(refname:short)' --count=1 refs/tags | sed -e 's/OneLife_v//'`
git checkout -q OneLife_v$latestMinorGemsVersion
echo "latest minorGems version = "${latestMinorGemsVersion}


if [ -d /root/game ];then
    echo "/root/game is exits"
    cp -rf /root/checkout/minorGems /root/game/
    cp -rf /root/checkout/OneLife /root/game/
    cp -rf /root/checkout/OneLifeData7 /root/game/
else 
    echo "mkdir /root/game"
    mkdir /root/game
    cp -rf /root/checkout/minorGems /root/game/
    cp -rf /root/checkout/OneLife /root/game/
    cp -rf /root/checkout/OneLifeData7 /root/game/

fi

echo "update code end"
