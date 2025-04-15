import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from blog.models import Post

try:
    post = Post.objects.get(title='Hello World')
    post.slug = 'hello-world'
    post.save()
    print(f'已更新文章 "{post.title}" 的slug: {post.slug}')
except Post.DoesNotExist:
    print('未找到 "Hello World" 文章')