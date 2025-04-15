#!/bin/bash

echo -e "\e[32mDjango 开发服务器启动脚本\e[0m"
echo -e "\e[32m-------------------------\e[0m"

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