from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class LatestPostsFeed(Feed):
    title = 'MyBlog 最新文章'
    link = '/'
    description = '个人博客最新更新'

    def items(self):
        return Post.objects.filter(status='published').order_by('-created_on')[:30]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt or item.content[:500]

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.created_on
