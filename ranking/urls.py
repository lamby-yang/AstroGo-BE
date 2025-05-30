# ranking/urls.py
from django.urls import path
from ranking.views import CampusRankingView

urlpatterns = [
    path('campus/', CampusRankingView.as_view(), name='campus'),
]