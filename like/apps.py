# like/apps.py
from django.apps import AppConfig

class LikeConfig(AppConfig):  # 修改类名与app名称对应
    default_auto_field = "django.db.models.BigAutoField"
    name = "like"
    label = "like_app"  # 添加唯一标签