# web_target/serializers.py
from rest_framework import serializers
from .models import ExerciseTarget

class ExerciseTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseTarget
        fields = '__all__'  # 或者指定需要的字段，如 ['target_id', 'uid', 'target_type', ...]