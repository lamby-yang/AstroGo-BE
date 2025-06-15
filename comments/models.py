# comments/models.py
from django.db import models
from django.utils import timezone

class Comment(models.Model):
    interact_id = models.AutoField(primary_key=True, verbose_name="交互ID")  # 使用interact_id作为主键
    uid = models.IntegerField(verbose_name="用户ID")
    post_id = models.IntegerField(verbose_name="帖子ID")
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name="父评论",
        db_column='parent_id'  # 明确指定数据库列名
    )
    content = models.TextField(verbose_name="评论内容")
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="创建时间",
        db_column='interact_time'  # 映射到数据库的interact_time字段
    )
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = 'SocialCommentInteraction'
        ordering = ['-created_at']
        verbose_name = '社交评论'
        verbose_name_plural = '社交评论'

    def __str__(self):
        return f"Comment {self.interact_id} by User {self.uid}"  # 更新为使用interact_id
