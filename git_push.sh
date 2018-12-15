#! /bin/bash
git add .
git commit -m "脚本自动提交"
read -p "等待！"
git push
