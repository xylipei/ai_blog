Write-Host "Django 开发服务器启动脚本" -ForegroundColor Green
Write-Host "-------------------------" -ForegroundColor Green

# 进入项目目录
Set-Location -Path .\myproject

# 激活虚拟环境（如果使用虚拟环境）
# & ..\venv\Scripts\Activate.ps1

# 运行迁移
Write-Host "执行数据库迁移..." -ForegroundColor Yellow
python manage.py migrate

# 启动服务器
Write-Host "启动开发服务器..." -ForegroundColor Yellow
python manage.py runserver

# 如果想自定义端口，可以使用下面的命令
# python manage.py runserver 8080

Pause