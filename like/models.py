from django.db import models
from web_profile.models import User

class SocialLikeInteraction(models.Model):
    like_id = models.AutoField(primary_key=True, db_column='like_id', verbose_name='点赞ID')
    uid = models.IntegerField(db_column='uid', verbose_name='用户ID')
    post_id = models.IntegerField(db_column='post_id', verbose_name='帖子ID')
    like_time = models.DateTimeField(db_column='like_time', verbose_name='点赞时间')

    class Meta:
        db_table = 'SocialLikeInteraction'
        verbose_name = '点赞互动'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"用户{self.uid} 点赞了帖子{self.post_id}"
