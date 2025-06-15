# ranking/models.py
from django.db import models

class DailyRanking(models.Model):
    uid = models.IntegerField()
    record_date = models.DateField()
    total_duration = models.IntegerField(default=0)  # 总运动时长（分钟）
    total_calorie = models.FloatField(default=0.0)   # 总卡路里

    class Meta:
        unique_together = ('uid', 'record_date')  # 确保每个用户每天只有一条记录
        ordering = ['-record_date']  # 按日期降序排列

    def __str__(self):
        return f"UID {self.uid} - {self.record_date}: {self.total_duration}min, {self.total_calorie}kcal"
# ranking/models.py
class WeeklyRanking(models.Model):
    week_start = models.DateField()  # 周的第一天（周一）
    uid = models.IntegerField()
    total_duration = models.IntegerField(default=0)
    total_calorie = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('week_start', 'uid')
        ordering = ['-week_start', '-total_calorie']

class MonthlyRanking(models.Model):
    month_start = models.DateField()  # 月的第一天
    uid = models.IntegerField()
    total_duration = models.IntegerField(default=0)
    total_calorie = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('month_start', 'uid')
        ordering = ['-month_start', '-total_calorie']

class ExerciseRecords(models.Model):
    record_id = models.AutoField(primary_key=True)
    uid = models.IntegerField()
    record_time = models.DateField()
    exercise_type = models.CharField(max_length=20)
    duration = models.IntegerField()
    distance = models.FloatField(blank=True, null=True)
    calorie = models.FloatField(blank=True, null=True)
    verification_photo_url = models.CharField(max_length=255, blank=True, null=True)
    verification_status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('pass', 'Pass'),
            ('fail', 'Fail')
        ]
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False  # 不让 Django 管理这个表
        db_table = 'ExerciseRecords'