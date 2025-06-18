# web_profile/models.py
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class User(models.Model):
    # ----------- 表字段映射 -----------
    uid = models.AutoField(primary_key=True, db_column='uid', verbose_name='用户ID')
    user_name = models.CharField(
        max_length=20,
        unique=True,
        db_column='user_name',
        verbose_name='用户名',
        default='admin'
    )
    pwd = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        db_column='pwd',  # 映射到数据库的 pwd 列
        verbose_name='密码',
    )
    creat_time = models.DateTimeField(
        default=timezone.now,
        db_column='creat_time',
        verbose_name='创建时间'
    )
    last_login_time = models.DateTimeField(
        null=True,
        blank=True,
        db_column='last_login_time',  # 映射到数据库列名
        verbose_name='最后登录时间'
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        db_column='phone_number',
        verbose_name='手机号',
        validators=[
            RegexValidator(
                regex=r'^1[3-9]\d{9}$',
                message="手机号码格式不正确"
            )
        ]
    )
    avatar_url = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column='avatar_url',
        verbose_name='头像URL'
    )
    department = models.IntegerField(
        null=True,
        blank=True,
        db_column='department',
        verbose_name='所属系'
    )
    age = models.IntegerField(
        null=True,
        blank=True,
        db_column='age',
        verbose_name='年龄'
    )
    height = models.IntegerField(
        null=True,
        blank=True,
        db_column='height',
        verbose_name='身高(cm)'
    )
    weight = models.IntegerField(
        null=True,
        blank=True,
        db_column='weight',
        verbose_name='体重(kg)'
    )

    class Meta:
        db_table = 'UserInfo'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user_name} ({self.phone_number})"