# web_target/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ExerciseTarget
from .serializers import ExerciseTargetSerializer  # 需要先创建序列化器

class ExerciseTargetsByUidView(APIView):
    """
    根据 uid 查询 ExerciseTargets 数据（返回 JSON 格式）
    """
    # 允许无需认证即可访问
    authentication_classes = []
    permission_classes = []

    def get(self, request, uid):
        try:
            targets = ExerciseTarget.objects.filter(uid=uid)
            serializer = ExerciseTargetSerializer(targets, many=True)  # many=True 表示序列化多个对象
            return Response(serializer.data)
        except ExerciseTarget.DoesNotExist:
            return Response(
                {"error": "未找到匹配的目标数据"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, uid):
        try:
            target = ExerciseTarget.objects.get(uid=uid)
            serializer = ExerciseTargetSerializer(target, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ExerciseTarget.DoesNotExist:
            return Response({"error": "目标不存在"}, status=status.HTTP_404_NOT_FOUND)