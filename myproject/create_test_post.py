import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Post

user = User.objects.first()
category = Category.objects.first()

# 创建第二篇测试文章
if not Post.objects.filter(slug='beautiful-design').exists():
    post = Post.objects.create(
        title='美丽的设计',
        slug='beautiful-design',
        author=user,
        content='# 博客设计的艺术\n\n一个好的博客设计应该兼顾美观和功能，使内容易于阅读和分享。\n\n## 设计原则\n\n- **简洁**：去除不必要的元素，专注于内容\n- **排版**：良好的字体选择和行间距\n- **响应式**：在各种设备上都能良好显示\n- **色彩**：和谐的配色方案增强视觉体验\n\n## 用户体验\n\n好的博客设计会考虑用户体验，包括导航的便捷性、阅读的舒适度和内容的可发现性。',
        category=category,
        status='published'
    )
    print(f'文章已创建：{post.title}')
else:
    print('第二篇文章已存在')

print('当前文章列表:')
for post in Post.objects.all():
    print(f'- {post.title} (slug: {post.slug})')