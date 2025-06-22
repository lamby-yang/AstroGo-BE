# gogogo/serializers.py
from rest_framework import serializers
from .models import ExerciseRecords

class ExerciseRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRecords  # 要序列化的模型
        fields = ['record_id', 'uid', 'exercise_type', 'record_time', 'duration', 'calorie', 'distance', 'verification_photo_url', 'verification_status']  # 需要返回的字段
