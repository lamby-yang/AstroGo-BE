# ranking/urls.py
from django.urls import path
from ranking.views import CampusRankingView
from .views import ExerciseRecordsView, ExerciseRecordDetailView

urlpatterns = [
    path('exercise-records/', ExerciseRecordsView.as_view(), name='exercise-records'),
    path('exercise-records/<int:pk>/', ExerciseRecordDetailView.as_view(), name='exercise-record-detail'),
    path('campus/', CampusRankingView.as_view(), name='campus'),
]