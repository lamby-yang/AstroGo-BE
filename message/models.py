from django.db import models
from web_profile.models import User as UserInfo

class ExerciseReminders(models.Model):
    reminder_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
        db_column='uid'
    )
    reminder_days_of_week=models.CharField(max_length=9)
    reminder_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'ExerciseReminders'


class ExerciseTargets(models.Model):
    TARGET_CHOICES = [
        ('day', '每日'),
        ('week', '每周'),
        ('month', '每月'),
    ]
    TYPE_CHOICES = [
        ('锻炼时长', '锻炼时长'),
        ('燃烧卡路里', '燃烧卡路里'),
    ]

    target_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
        db_column='uid'
    )
    target_cycle = models.CharField(max_length=10, choices=TARGET_CHOICES)
    target_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    target_duration = models.IntegerField(null=True, blank=True)
    target_calorie = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'ExerciseTargets'
        ordering = ['-target_id']


class ExerciseRecords(models.Model):
    record_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
        db_column='uid'
    )
    record_time = models.DateTimeField()
    duration = models.IntegerField()
    calorie = models.FloatField()
    is_deleted = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=10,
        choices=[('pending', '待审核'), ('pass', '通过'), ('reject', '拒绝')],
        default='pending'
    )

    class Meta:
        db_table = 'ExerciseRecords'