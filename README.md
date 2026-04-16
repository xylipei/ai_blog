# AI 个人博客（Django）

将 **AI 对话** 与 **Markdown 博客** 结合：访客除阅读文章外，可通过侧栏对话接口（`POST /api/chat/`）与博客助手交互；后端使用 LangChain + OpenAI 兼容 API，**流式**返回中文回复。模型与提示词见 [`myproject/blog/chat.py`](myproject/blog/chat.py)。

## 功能

- **博客**：文章（Markdown）、分类、标签、归档、搜索、RSS、评论、关于页、简历页（Markdown）
- **AI**：需配置环境变量 `OPENAI_API_KEY`；未配置时聊天不可用，其余页面正常

## 环境

- Python 3.12+、Django 5.2；依赖见 [`requirements.txt`](requirements.txt)
- 数据库：开发可用 SQLite；生产建议 MySQL（`utf8mb4`），变量见 `myproject/myproject/settings.py`

## 快速开始

```bash
git clone <repository-url> && cd <project-root>
python -m venv venv && venv\Scripts\activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

根目录创建 `.env`，配置数据库变量及 `OPENAI_API_KEY`。

```bash
cd myproject
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

仓库根目录也可用 `run_server.bat`（Windows）启动。

访问：<http://127.0.0.1:8000/> ，后台：<http://127.0.0.1:8000/admin/>

## 目录

| 路径 | 说明 |
|------|------|
| `myproject/` | 项目配置与根路由 |
| `myproject/blog/` | 博客应用与 AI 聊天接口 |
| `myproject/templates/`、`myproject/static/` | 模板与静态资源 |
| `media/` | 上传媒体 |

## 生产部署

使用 WSGI/ASGI 托管，设置 `DEBUG=False`、`ALLOWED_HOSTS`，勿提交 `.env` 与密钥。
