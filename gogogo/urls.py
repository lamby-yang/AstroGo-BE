from django.urls import path
from . import views
from .views import ExerciseRecordsByTimeRangeView

urlpatterns = [
    path('api/exercise/submit', views.submit_exercise_record, name='submit_exercise_record'),
    path('api/exercise/records', views.get_exercise_records, name='get_exercise_records'),
     path('api/exercise-records/time-range/', ExerciseRecordsByTimeRangeView.as_view(), name='exercise-records-by-time-range'),
     path('api/exercise/timeRange', views.get_time_records, name='get_time_records'),
]
