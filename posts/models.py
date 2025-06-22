from django.db import models
from web_profile.models import User as UserInfo  # 替换为你的用户模型路径

class SocialMediaPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(
        UserInfo,
        on_delete=models.CASCADE,
        db_column='uid',
        related_name='media'
    )
    post_content = models.TextField()
    post_time = models.DateTimeField(auto_now_add=True)  # 自动填充时间
    post_title = models.TextField(max_length=255)  # 匹配 TEXT 类型
    post_image = models.JSONField(null=True, blank=True, default=None)  # 默认 NULL
    like_count = models.IntegerField(default=0)
    VERIFICATION_CHOICES = [
        ('pass', '审核通过'),
        ('pending', '审核中'),
        ('fail', '审核未通过'),
    ]
    verification_status = models.CharField(
        max_length=10,
        choices=VERIFICATION_CHOICES,
        default='pending'
    )

    class Meta:
        db_table = 'SocialMediaPost'
        ordering = ['-post_time']  # 默认按时间倒序排序