# Generated by Django 5.2.1 on 2025-05-16 17:07

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "uid",
                    models.AutoField(
                        db_column="uid",
                        primary_key=True,
                        serialize=False,
                        verbose_name="用户ID",
                    ),
                ),
                (
                    "user_name",
                    models.CharField(
                        db_column="user_name",
                        default="admin",
                        max_length=20,
                        unique=True,
                        verbose_name="用户名",
                    ),
                ),
                (
                    "pwd",
                    models.CharField(
                        blank=True,
                        db_column="pwd",
                        max_length=128,
                        null=True,
                        verbose_name="密码",
                    ),
                ),
                (
                    "creat_time",
                    models.DateTimeField(
                        db_column="creat_time",
                        default=django.utils.timezone.now,
                        verbose_name="创建时间",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        db_column="phone_number",
                        max_length=20,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="手机号码格式不正确", regex="^1[3-9]\\d{9}$"
                            )
                        ],
                        verbose_name="手机号",
                    ),
                ),
                (
                    "avatar_url",
                    models.CharField(
                        blank=True,
                        db_column="avatar_url",
                        max_length=255,
                        null=True,
                        verbose_name="头像URL",
                    ),
                ),
                (
                    "department",
                    models.IntegerField(
                        blank=True,
                        db_column="department",
                        null=True,
                        verbose_name="所属系",
                    ),
                ),
                (
                    "age",
                    models.IntegerField(
                        blank=True, db_column="age", null=True, verbose_name="年龄"
                    ),
                ),
                (
                    "height",
                    models.IntegerField(
                        blank=True,
                        db_column="height",
                        null=True,
                        verbose_name="身高(cm)",
                    ),
                ),
                (
                    "app_id",
                    models.CharField(
                        blank=True,
                        db_column="app_id",
                        max_length=100,
                        null=True,
                        verbose_name="应用ID",
                    ),
                ),
            ],
            options={
                "verbose_name": "用户信息",
                "verbose_name_plural": "用户信息",
                "db_table": "UserInfo",
            },
        ),
    ]
