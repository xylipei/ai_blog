# Django 项目

这是一个使用 Django 5.2 构建的 Web 应用程序。

## 环境要求

- Python 3.12 或更高版本
- Django 5.2
- 其他依赖项可查看 requirements.txt (如有)

## 快速开始

1. 克隆项目:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. 创建并激活虚拟环境 (可选):
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/macOS
   ```

3. 安装依赖:
   ```
   pip install -r requirements.txt  # 如果存在requirements.txt
   ```

4. 运行服务器:
   ```
   # 使用批处理文件 (Windows)
   run_server.bat
   
   # 或使用PowerShell脚本 (Windows)
   .\run_server.ps1
   
   # 或手动运行
   cd myproject
   python manage.py migrate
   python manage.py runserver
   ```

5. 访问网站:
   浏览器中打开 http://127.0.0.1:8000/

## 目录结构

- `myproject/` - Django 项目目录
  - `myproject/` - 项目设置和主要URL配置
  - `blog/` - 博客应用
  - `templates/` - HTML模板
  - `static/` - 静态文件 (CSS, JavaScript, 图片等)
  - `media/` - 用户上传的媒体文件

## 开发服务器

开发服务器默认在 http://127.0.0.1:8000/ 运行