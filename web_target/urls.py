# web_target/urls.py

from django.urls import path
from .views import ExerciseTargetsByUidView

urlpatterns = [
    path('<int:uid>/', ExerciseTargetsByUidView.as_view(), name='exercise_targets_by_uid'),
]
