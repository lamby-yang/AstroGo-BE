# gogogo/models.py
from django.db import models
from web_profile.models import User  # 导入 User 模型


class ExerciseRecords(models.Model):
    # 用户外键，指向 User 模型中的 uid 字段
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uid', verbose_name="用户ID", related_name="gogogo_exercise_records")
    
    # 记录ID，自增主键
    record_id = models.AutoField(primary_key=True, verbose_name="记录ID")
    
    # 运动时间
    record_time = models.DateTimeField(auto_now_add=True, verbose_name="运动时间")
    
    # 运动类型
    exercise_type = models.CharField(max_length=20, choices=[
        ('running', '跑步'),
        ('walking', '竞走'),
        ('yoga', '瑜伽'),
        ('cycling', '骑车'),
        ('badminton', '羽毛球'),
        ('basketball', '篮球'),
        ('football', '足球'),
        ('swimming', '游泳')
    ], verbose_name="运动类型")
    
    # 运动时长，单位为分钟
    duration = models.IntegerField(verbose_name="运动时长(分钟)")
    
    # 运动距离，单位为公里
    distance = models.FloatField(verbose_name="运动距离(km)", null=True)
    
    # 运动消耗的卡路里
    calorie = models.FloatField(verbose_name="消耗卡路里(kcal)", null=True)
    
    # 运动验证图片的URL
    verification_photo_url = models.URLField(null=True, blank=True, verbose_name="验证照片URL")
    
    # 运动记录的验证状态，是否通过验证
    verification_status = models.CharField(max_length=10, choices=[
        ('pending', '待审核'),
        ('approved', '通过'),
        ('rejected', '未通过')
    ], default='pending', verbose_name="验证状态")
    
    # 是否已删除标志
    is_deleted = models.BooleanField(default=False, verbose_name="是否已删除")

    class Meta:
        db_table = "ExerciseRecords"
        verbose_name = "运动记录"
        managed = False
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"运动记录 {self.record_id} 用户 {self.uid.user_name} - {self.exercise_type}"
