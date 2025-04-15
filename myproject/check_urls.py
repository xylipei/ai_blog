import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.urls import reverse
from blog.models import Post

for post in Post.objects.all():
    print(f'文章: {post.title}')
    print(f'Slug: {post.slug}')
    print(f'URL: {post.get_absolute_url()}')
    print(f'Reverse URL: {reverse("post_detail", args=[post.slug])}')
    print('-' * 50)