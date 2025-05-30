# web_target/models.py

from django.db import models

class ExerciseTarget(models.Model):

    TARGET_TYPE_CHOICES = [
        ('duration', 'Duration'),
        ('calorie', 'Calorie'),
    ]

    target_id = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    target_type = models.CharField(
        max_length=8,
        choices=TARGET_TYPE_CHOICES,
        default='duration',
    )
    target_cycle = models.CharField(
        max_length=5,
        choices=[('day', 'day'), ('week', 'week'), ('month', 'month')],
        default='day'
    )
    target_duration = models.IntegerField(null=True, blank=True)
    target_calorie = models.FloatField(null=True, blank=True)

    class Meta:
        managed = False  # 不让 Django 管理数据库迁移
        db_table = 'ExerciseTargets'  # 指定数据库表名

    def __str__(self):
        return f"{self.target_type} ({self.target_cycle})"