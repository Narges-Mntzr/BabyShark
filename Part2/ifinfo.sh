#!/bin/bash
touch info.txt
echo $1 >> info.txt
echo $2 >> info.txt
echo $(ip -f inet addr show $3 | sed -En -e 's/.*inet ([0-9.]+).*/\1/p') >> info.txt
echo $4 >> info.txt
echo $3 >> info.txt
echo $(ifconfig $3 | grep -o -E ..:..:..:..:..:.. | sed 's/:/ /g')>> info.txt
echo $(arp -n | grep `route -n | awk '/UG/{print $2}'` | awk '{print $3}'| sed 's/:/ /g') >> info.txt 