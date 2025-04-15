from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('category/<str:category>/', views.CategoryView.as_view(), name='category'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('search/', views.search_posts, name='search'),
] 