# ranking/serializers.py
from rest_framework import serializers
from .models import ExerciseRecords
from datetime import date


class ExerciseRecordSerializer(serializers.ModelSerializer):
    record_time = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])

    class Meta:
        model = ExerciseRecords
        fields = [
            'record_id',
            'uid',
            'record_time',
            'exercise_type',
            'duration',
            'distance',
            'calorie',
            'verification_photo_url',
            'verification_status',
            'is_deleted'
        ]

        extra_kwargs = {
            'distance': {'allow_null': True},
            'calorie': {'allow_null': True},
            'verification_photo_url': {'allow_null': True},
            'record_id': {'read_only': True},  # 记录ID只读
        }

    def validate_record_time(self, value):
        """确保日期不是未来日期"""
        if value > date.today():
            raise serializers.ValidationError("记录日期不能是未来日期")
        return value

    def validate_duration(self, value):
        """确保时长是正数"""
        if value <= 0:
            raise serializers.ValidationError("运动时长必须大于0")
        return value