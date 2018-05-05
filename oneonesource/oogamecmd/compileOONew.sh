#!/bin/sh

echo "start update code and data..."
sh /root/checkout/updatecode.sh

echo "code and data update end"

echo "start compile server"

cd /root/game/OneLife/server
./configure 1
make


ln -s ../../OneLifeData7/categories .
ln -s ../../OneLifeData7/objects .
ln -s ../../OneLifeData7/transitions .
ln -s ../../OneLifeData7/dataVersionNumber.txt .


git for-each-ref --sort=-creatordate --format '%(refname:short)' --count=1 refs/tags | sed -e 's/OneLife_v//' > serverCodeVersionNumber.txt

echo 0 > settings/requireTicketServerCheck.ini
echo 1 > settings/forceEveLocation.ini

