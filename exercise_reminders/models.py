from django.db import models
#
# class ExerciseReminders(models.Model):
#     reminder_id = models.AutoField(primary_key=True)
#     uid = models.IntegerField()  # 整数类型的 UID（无关联外键）
#     reminder_days_of_week = models.CharField(max_length=8)  # 如 "0101010"
#     reminder_time = models.TimeField()
#     is_active = models.BooleanField(default=True)
#
#     class Meta:
#         db_table = 'ExerciseReminders'  # 指定数据库表名