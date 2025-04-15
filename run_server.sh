#!/bin/bash

echo -e "\e[32mDjango 开发服务器启动脚本\e[0m"
echo -e "\e[32m-------------------------\e[0m"

# 检查是否安装了python3-venv
if ! rpm -q python3-venv &>/dev/null; then
    echo -e "\e[31m未安装python3-venv，正在安装...\e[0m"
    sudo yum install -y python3-venv
fi

# 检查虚拟环境是否存在，如果不存在则创建
if [ ! -d "venv" ]; then
    echo -e "\e[33m创建虚拟环境...\e[0m"
    python3 -m venv venv
fi

# 激活虚拟环境
echo -e "\e[33m激活虚拟环境...\e[0m"
source venv/bin/activate

# 安装或更新依赖
if [ -f "requirements.txt" ]; then
    echo -e "\e[33m安装依赖...\e[0m"
    pip install -r requirements.txt
fi

# 进入项目目录
cd ./myproject

# 运行迁移
echo -e "\e[33m执行数据库迁移...\e[0m"
python manage.py migrate

# 启动服务器
echo -e "\e[33m启动开发服务器...\e[0m"
python manage.py runserver

# 如果想自定义端口，可以使用下面的命令
# python manage.py runserver 8080

# 按任意键继续
read -n 1 -s -r -p "按任意键继续..."