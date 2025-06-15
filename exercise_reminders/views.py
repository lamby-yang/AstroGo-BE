from rest_framework import generics
from message.models import ExerciseReminders
from .serializers import ExerciseReminderSerializer
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import TokenAuthentication

class ExerciseReminderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExerciseReminderSerializer
    authentication_classes = [TokenAuthentication]  # 添加认证类
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'reminder_id'

    def get_queryset(self):
        return ExerciseReminders.objects.filter(uid=self.request.user.id)

    def get_object(self):
        obj = super().get_object()

        # 更详细的权限检查
        if obj.uid != self.request.user.id:
            self.raise_not_found_or_permission_denied()

        return obj

    def raise_not_found_or_permission_denied(self):
        # 防止通过错误信息泄露数据存在性
        raise PermissionDenied("资源不存在或您无访问权限")
class ExerciseReminderListCreate(generics.ListCreateAPIView):
    serializer_class = ExerciseReminderSerializer

    def get_queryset(self):
        uid = self.kwargs['uid']  # 从 URL 获取 uid
        return ExerciseReminders.objects.filter(uid=uid)

