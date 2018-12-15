#! /bin/bash

pro="0"

input_fun(){
    echo "------------------------------------------------------------------------"
    echo -e "操作列表：\n\t0:退出\n\t1:提交代码\n\t2:更新代码\n\t3:重新打包\n\t4:停止服务\n\t5:内网部署\n\t6:启动服务\n\t7:测试服务\n\t8:提交包体"
    read -p "输入要执行的操作：" pro
    echo -e "\n"
    echo "执行的操作为$pro"
}

cond_fun(){
    echo "判断"
    if [ "$pro" = "1" ];then
        echo "提交代码"
        cd /home/DMATAPP/feature/python_package
        ./git_push.sh
    elif [ "$pro" = "2" ];then
        echo "更新代码"
        cd /home/DMATAPP/feature/python_package
        ./git_pull.sh
    elif [ "$pro" = "3" ];then
        echo "重新打包"
        cd /home/DMATAPP/feature/python_package/package
        ./package.sh
    elif [ "$pro" = "4" ];then
        echo "停止服务"
        cd /home/DMATAPP/feature/python_package/package/linux
        ./stop.sh
    elif [ "$pro" = "5" ];then
        echo "内网部署"
        cd /home/DMATAPP/feature/python_package/package
        ./deploy_linux.sh
    elif [ "$pro" = "6" ];then
        echo "启动服务"
        cd /home/DMATAPP/application/python_package
        ./start.sh
    elif [ "$pro" = "7" ];then
        echo "测试服务"
        cd /home/DMATAPP/feature/python_package/package/linux
        ./test.sh
    elif [ "$pro" = "8" ];then
        echo "提交包体"
        cd /home/DMATAPP/feature/python_package/package
        ./beta_push.sh
    fi
}

# 主函数
main_fun(){
    input_fun
    while [ $pro -ne "0" ]
    do
    cond_fun
    input_fun
    done
}

echo "-------命令操作集-------"
main_fun
