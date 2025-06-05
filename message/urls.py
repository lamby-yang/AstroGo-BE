from django.urls import path
from . import views

urlpatterns = [
    path('login_user/', views.login_user),
    path('register_user/', views.register_user),
    path('user_info/<int:uid>/', views.user_info),
    path('exercise_reminders/<int:uid>/', views.exercise_reminders),
    path('check_phone/<str:phone_number>/', views.check_phone),
    path('exercise_overview/<int:uid>/', views.exercise_overview),
]