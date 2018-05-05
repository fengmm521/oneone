#!/bin/sh

cd /root/checkout

if [ -f minorGems.zip ];then
   	rm minorGems.zip
   	rm OneLife.zip
	rm categories.zip
	rm objects.zip
	rm transitions.zip
fi

zip -r minorGems.zip minorGems/

zip -r OneLife.zip OneLife/

zip -r categories.zip OneLifeData7/categories/

zip -r objects.zip OneLifeData7/objects/

zip -r transitions.zip OneLifeData7/transitions
