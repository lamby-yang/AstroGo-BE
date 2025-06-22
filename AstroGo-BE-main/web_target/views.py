from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ExerciseTarget
from .serializers import ExerciseTargetSerializer

class ExerciseTargetsByUidView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, uid):
        targets = ExerciseTarget.objects.filter(uid=uid)
        serializer = ExerciseTargetSerializer(targets, many=True)
        return Response(serializer.data)

    def post(self, request, uid):
        serializer = ExerciseTargetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uid=uid)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, uid):
        try:
            target = ExerciseTarget.objects.get(uid=uid)
            serializer = ExerciseTargetSerializer(target, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ExerciseTarget.DoesNotExist:
            return self.post(request, uid)  # 如果不存在则创建