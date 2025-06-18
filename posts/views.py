from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import SocialMediaPost
from .serializers import SocialMediaPostSerializer


class SocialMediaPostListCreateView(generics.ListCreateAPIView):
    """获取帖子列表 """
    serializer_class = SocialMediaPostSerializer
    # permission_classes = [permissions.IsAuthenticated]  # 要求用户认证

    def get_queryset(self):
        # 按用户ID过滤（可选，按需添加）
        # uid = self.request.query_params.get('uid', None)
        # if uid is not None:
        #     return SocialMediaPost.objects.filter(uid=uid)
        return SocialMediaPost.objects.all()




class SocialMediaPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """获取、更新、删除单个帖子"""
    queryset = SocialMediaPost.objects.all()
    serializer_class = SocialMediaPostSerializer
    # permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'post_id'  # 使用 post_id 作为查询标识符