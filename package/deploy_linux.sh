#! /bin/bash

echo "-------------开始部署服务---------------------"
# 删除工程
rm -rf /home/DMATAPP/application/security_center

# 复制
cp -r build/exe.linux-x86_64-3.6 /home/DMATAPP/application/security_center
echo "-------------部署服务结束---------------------"



