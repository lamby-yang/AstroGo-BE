# web_profile/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:user_id>/', views.PublicUserProfileView.as_view(), name='public-user-profile'),
]