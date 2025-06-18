# comment_list/models.py

from django.db import models
from web_profile.models import User  # 导入 User 模型

class SocialMediaPost(models.Model):
    # 用户外键，指向 User 模型中的 uid 字段
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uid', verbose_name='发布用户ID')  # 使用 User 作为外键
    post_id = models.IntegerField(primary_key=True, verbose_name='帖子ID')  # 帖子ID
    post_time = models.DateTimeField(auto_now_add=True, verbose_name='帖子发布时间')
    post_title = models.TextField(verbose_name='帖子标题')
    post_content = models.TextField(verbose_name='帖子内容')
    post_image = models.JSONField(null=True, blank=True, verbose_name='帖子图片')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    verification_status = models.CharField(
        max_length=10,
        choices=[('pending', '待审核'), ('approved', '通过'), ('rejected', '未通过')],
        default='pending',
        verbose_name='认证状态'
    )

    def __str__(self):
        return f"Post {self.post_id} by User {self.uid}"

    class Meta:
        db_table = 'SocialMediaPost'
        ordering = ['-post_time']
        managed = False


class SocialCommentInteraction(models.Model):
    interact_id = models.AutoField(primary_key=True)  # 评论 ID，自增主键
    # 使用完整路径来引用 User 模型
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uid', verbose_name='互动用户 ID')  # 使用 User 作为外键
    post_id = models.ForeignKey(SocialMediaPost, on_delete=models.CASCADE, db_column='post_id', verbose_name='互动帖子 ID')  # 显式指定db_column为post_id  # 外键关联到帖子
    parent_id = models.IntegerField(null=True, blank=True, verbose_name='父评论 ID')  # 父评论 ID，允许为空
    content = models.TextField(verbose_name='评论内容')  # 评论内容
    interact_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')  # 评论时间，自动设置为当前时间

    class Meta:
        db_table = 'SocialCommentInteraction'
        ordering = ['-interact_time']
        managed = False

    def __str__(self):
        return f'评论 ID: {self.interact_id}, 用户 ID: {self.uid}'
