from rest_framework import serializers
from .models import SocialMediaPost

class SocialMediaPostSerializer(serializers.ModelSerializer):
    post_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = SocialMediaPost
        fields = '__all__'
        read_only_fields = ('post_id', 'like_count', 'post_time')  # 这些字段不可修改

    # 可选：自定义验证
    def validate_verification_status(self, value):
        """验证状态只能是预定值"""
        if value not in ['pass', 'pending', 'fail']:
            raise serializers.ValidationError("Invalid verification status")
        return value