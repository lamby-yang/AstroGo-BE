# web_profile/serializers.py
from rest_framework import serializers
from .models import User

allowed_ids = (
        list(range(1, 22)) +  # 1-21
        list(range(23, 33)) +  # 23-32
        [35] +  # 35
        list(range(37, 40)) +  # 37-39
        list(range(41, 44))  # 41-43
)


class UserSerializer(serializers.ModelSerializer):
    # 时间字段直接映射（模型字段已重命名）
    creat_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True
    )
    last_login_time = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            'uid',  # 对应数据库的 uid 字段
            'user_name',  # 原 username 字段
            'creat_time',
            'last_login_time',
            'phone_number',
            'avatar_url',
            'department',
            'age',
            'height',  # 注意数据库中是 INT 类型
            'pwd',
            'open_id',  # 新增必须包含的字段
        ]
        read_only_fields = (
            'uid',
            'creat_time',
            'last_login_time',
        )
