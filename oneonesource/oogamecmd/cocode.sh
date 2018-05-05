#!/bin/sh

if [ -d /root/checkout ];then
	echo "/root/checkout is exits"
else
  	echo "mkdir /root/checkout"
    mkdir /root/checkout
fi

cd /root/checkout

if [ ! -e minorGems ]
then
	git clone https://github.com/jasonrohrer/minorGems.git	
fi

if [ ! -e OneLife ]
then
	git clone https://github.com/jasonrohrer/OneLife.git
fi

if [ ! -e OneLifeData7 ]
then
	git clone https://github.com/jasonrohrer/OneLifeData7.git	
fi


cd minorGems
git fetch --tags
latestTaggedVersion=`git for-each-ref --sort=-creatordate --format '%(refname:short)' --count=1 refs/tags | sed -e 's/OneLife_v//'`
git checkout -q OneLife_v$latestTaggedVersion

echo "latestTaggedVersion="${latestTaggedVersion}

cd ../OneLife
git fetch --tags
latestTaggedVersionA=`git for-each-ref --sort=-creatordate --format '%(refname:short)' --count=1 refs/tags | sed -e 's/OneLife_v//'`
git checkout -q OneLife_v$latestTaggedVersionA

echo "latestTaggedVersionA="${latestTaggedVersionA}

cd ../OneLifeData7
git fetch --tags
latestTaggedVersionB=`git for-each-ref --sort=-creatordate --format '%(refname:short)' --count=1 refs/tags | sed -e 's/OneLife_v//'`
git checkout -q OneLife_v$latestTaggedVersionB

echo "latestTaggedVersionB="${latestTaggedVersionB}

rm */cache.fcz


latestVersion=$latestTaggedVersionB


if [ $latestTaggedVersionA -gt $latestTaggedVersionB ]
then
	latestVersion=$latestTaggedVersionA
fi

echo "latestVersion="${latestVersion}

