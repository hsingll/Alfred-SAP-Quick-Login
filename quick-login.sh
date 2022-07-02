#!/bin/bash

# set -e

QUERY=`echo $1`
PATH=/usr/local/bin:$PATH

RESULT=`prlctl exec $VM_UUID --current-user sapshcut.exe $QUERY 2>&1`

echo $RESULT
if [[ -n "$RESULT" ]] 
then 
    echo $RESULT
else     
    echo "已发送快捷登录命令，请至虚拟机中操作！"
fi