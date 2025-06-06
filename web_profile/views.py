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


# 新增获取所有用户的API视图
class AllUsersProfileView(APIView):
    # 允许无需认证即可访问
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        try:
            # 获取所有用户
            users = User.objects.all()

            # 序列化用户数据
            serializer = UserSerializer(users, many=True)

            # 格式化响应数据
            response_data = {
                "code": 0,
                "msg": "success",
                "data": serializer.data
            }

            return Response(response_data)

        except Exception as e:
            # 错误处理
            return Response({
                "code": -1,
                "msg": f"系统错误: {str(e)}",
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

