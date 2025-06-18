from message.models import ExerciseReminders
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import ExerciseReminderSerializer


class ExerciseReminderUpdateView(generics.GenericAPIView):
    serializer_class = ExerciseReminderSerializer

    def post(self, request, *args, **kwargs):
        # 从URL参数获取要更新的提醒ID
        reminder_id = kwargs.get('reminder_id')

        try:
            # 获取要更新的提醒对象
            instance = ExerciseReminders.objects.get(reminder_id=reminder_id)
        except ExerciseReminders.DoesNotExist:
            raise NotFound(f"Exercise reminder with ID {reminder_id} not found")

        # 部分更新（允许只传递需要修改的字段）
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            # 保存更新
            serializer.save()
            return Response({
                'success': True,
                'message': 'Exercise reminder updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        # 处理无效数据
        return Response({
            'success': False,
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ExerciseReminderListCreate(generics.ListCreateAPIView):
    serializer_class = ExerciseReminderSerializer

    def get_queryset(self):
        uid = self.kwargs['uid']  # 从 URL 获取 uid
        return ExerciseReminders.objects.filter(uid=uid)




