#! /bin/bash

echo "-------------开始提交beat包---------------------"

# 复制
echo "复制"
v_date=$(date "+%Y%m%d%H%M%S")
package_name="beta_"${v_date}".zip"
cp -r build/beta.zip /home/DMATAPP/feature/package/python_package/${package_name}

# 提交
echo "提交"
cd /home/DMATAPP/feature/package/python_package
./git_push.sh
echo "####版本号####"
echo ${package_name}
echo "####版本号####"
echo "-------------提交beat包结束---------------------"



