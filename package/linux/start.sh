#!/bin/bash

function findpid()
{
	echo "查找pid"
        pid=`netstat -lntp | grep $1 | awk '{print $7}' | cut -d / -f1`
	if [ $? -eq 0 ];then 
		echo $pid
        	kill -9 $pid
	fi
}

function start()
{
	echo "启动服务"
	nohup ./main &
}

echo "-------------开始启动服务---------------------"
findpid 15011
start
sleep 1s
echo "-------------启动服务结束---------------------"

