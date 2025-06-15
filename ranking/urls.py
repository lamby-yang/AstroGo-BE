# ranking/urls.py
from django.urls import path
from ranking.views import CampusRankingView
from .views import ExerciseRecordsView, ExerciseRecordDetailView

urlpatterns = [
    path('exercise-records/<int:uid>/', ExerciseRecordsView.as_view(), name='user-exercise-records'),
    path('exercise-record/<int:pk>/', ExerciseRecordDetailView.as_view(), name='exercise-record-detail'),
    path('campus/', CampusRankingView.as_view(), name='campus'),
]