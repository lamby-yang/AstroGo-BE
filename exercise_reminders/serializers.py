from rest_framework import serializers
from message.models import ExerciseReminders

class ExerciseReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseReminders
        fields = '__all__'