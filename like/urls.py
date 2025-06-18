from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:user_id>/', views.PublicUserProfileView.as_view(), name='public-user-profile'),
    path('likes/', views.LikeListView.as_view(), name='like-list'),

    # 新增：获取该用户发布的帖子所收到的点赞
    path('likes/received/<int:user_id>/', views.UserReceivedLikesView.as_view(), name='received-likes'),
]
