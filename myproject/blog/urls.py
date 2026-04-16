from django.urls import path

from . import views, chat
from .feeds import LatestPostsFeed

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('resume/', views.resume, name='resume'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/<str:category>/', views.CategoryView.as_view(), name='category'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('search/', views.search_posts, name='search'),
    path('archive/', views.archive_index, name='archive'),
    path('archive/<int:year>/<int:month>/', views.ArchiveMonthView.as_view(), name='archive_month'),
    path('tag/<slug:slug>/', views.TagView.as_view(), name='tag'),
    path('feed/rss/', LatestPostsFeed(), name='post_feed'),
    path('api/chat/', chat.chat_with_ai, name='chat_with_ai'),
]
