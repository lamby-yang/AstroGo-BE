# comments/serializers.py
from rest_framework import serializers
from .models import Comment


class FlatCommentSerializer(serializers.ModelSerializer):
    parent_id = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['interact_id', 'uid', 'post_id', 'parent_id', 'content', 'created_at' , 'is_deleted']

    def get_username(self, obj):
        return f"User{obj.uid}"

    def get_parent_id(self, obj):
        return obj.parent.interact_id if obj.parent else None

class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    replies = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['interact_id', 'uid', 'post_id', 'parent', 'content', 'created_at', 'replies','is_deleted']
        extra_kwargs = {
            'parent': {'write_only': True}  # 父ID只用于写入，不显示在输出中
        }

    def get_username(self, obj):
        # 实际项目中这里应该查询用户表获取用户名
        return f"User{obj.uid}"

