from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('category/<str:category>/', views.CategoryView.as_view(), name='category'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('search/', views.search_posts, name='search'),
    path('api/chat/', views.chat_with_ai, name='chat_with_ai'),
]