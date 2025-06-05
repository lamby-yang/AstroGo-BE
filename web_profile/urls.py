# web_profile/urls.py
from django.urls import path
from .views import PublicUserProfileView, AllUsersProfileView

urlpatterns = [
    path('user/<int:user_id>/', PublicUserProfileView.as_view(), name='public-user-profile'),
    path('user/all/', AllUsersProfileView.as_view(), name='all-users-profile'),
]
