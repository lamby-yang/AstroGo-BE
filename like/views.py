# web_profile/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class PublicUserProfileView(APIView):
    # 允许无需认证即可访问
    authentication_classes = []
    permission_classes = []

    def get(self, request, user_id):
        try:
            # user = User.objects.get(id=user_id)
            user = User.objects.get(uid=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"error": "用户不存在"},
                status=status.HTTP_404_NOT_FOUND
            )

from .models import SocialLikeInteraction
from .serializers import LikeSerializer

class LikeListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        likes = SocialLikeInteraction.objects.all().order_by('-like_id')[:50]

        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)
