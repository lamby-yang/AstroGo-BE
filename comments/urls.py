# comments/urls.py
from django.urls import path
from .views import CommentListCreateView, CommentDetailView, FlatCommentListView

urlpatterns = [
    path('comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('flat-comments/', FlatCommentListView.as_view(), name='flat-comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comments/post/<int:post_id>/', CommentListCreateView.as_view(), name='post-comments'),
]