# web_profile/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SocialLikeInteraction
from .serializers import LikeSerializer

class LikeListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        likes = SocialLikeInteraction.objects.all().order_by('-like_id')[:50]

        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)
