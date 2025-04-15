@echo off
echo Django 开发服务器启动脚本
echo -------------------------

:: 进入项目目录
cd myproject

:: 激活虚拟环境（如果使用虚拟环境）
:: call ..\venv\Scripts\activate

:: 运行迁移
echo 执行数据库迁移...
python manage.py migrate

:: 启动服务器
echo 启动开发服务器...
python manage.py runserver

:: 如果想自定义端口，可以使用下面的命令
:: python manage.py runserver 8080

pause