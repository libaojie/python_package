#! /bin/bash

echo "-------------开始打包---------------------"
# 打包
echo "删除原打包环境"
rm -rf build
echo "打包"
python -m pipenv run python setup.py build

# 压缩包体
echo "压缩内部测试版"
zip -r build/alpha.zip build/exe.linux-x86_64-3.6

# 正式包
echo "压缩外部测试版"
cp -arf build/exe.linux-x86_64-3.6 build/beta
cp -arf linux/config/config.py build/beta
cd build
zip -r beta.zip beta
rm -rf beta
echo "-------------打包结束---------------------"
