# comment_list/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 路由: 获取用户的所有评论
    path('comments/', views.get_user_comments, name='get_user_comments'),
]
