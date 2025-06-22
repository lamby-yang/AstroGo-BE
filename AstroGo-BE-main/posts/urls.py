from django.urls import path
from . import views

urlpatterns = [
    # 帖子列表和创建
    path('posts/', views.SocialMediaPostListCreateView.as_view(), name='post-list-create'),

    # 单个帖子操作
    path('posts/<int:post_id>/', views.SocialMediaPostDetailView.as_view(), name='post-detail'),
]