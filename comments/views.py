# comments/views.py
from rest_framework import generics, permissions
from .models import Comment
from .serializers import CommentSerializer, FlatCommentSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = FlatCommentSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.kwargs.get('post_id')

        if post_id:
            queryset = queryset.filter(post_id=post_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(uid=self.request.user.id)  # 假设使用用户系统


class FlatCommentListView(generics.ListAPIView):
    serializer_class = FlatCommentSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Comment.objects.all()

        # 可选过滤条件
        post_id = self.request.query_params.get('post_id')
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)

        return queryset


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = FlatCommentSerializer  # 使用新的扁平化序列化器
    permission_classes = []

    def perform_destroy(self, instance):
        # 实现软删除
        instance.is_deleted = True
        instance.save()