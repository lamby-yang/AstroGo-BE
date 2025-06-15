from django.urls import path
from .views import ExerciseReminderListCreate, ExerciseReminderRetrieveUpdateDestroy

urlpatterns = [
    # 根据 uid 获取所有提醒或创建新提醒
    path('reminders/<int:uid>/', ExerciseReminderListCreate.as_view()),
    # 对单个提醒的详细操作 (需传递 reminder_id)
    path('reminder/<int:reminder_id>/', ExerciseReminderRetrieveUpdateDestroy.as_view()),
]