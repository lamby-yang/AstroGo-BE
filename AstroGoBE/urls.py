"""
URL configuration for AstroGoBE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # 新增导入

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('message.urls')),
    path('api/', include('posts.urls')),
    path('api/', include('like.urls')),
    path('api/', include('comments.urls')),
    path('api/', include('exercise_reminders.urls')),
    path('api/', include('web_profile.urls')),  # 包含应用路由
    path('api/auth/', include('rest_framework.urls')),  # 启用DRF登录
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('comment_list.urls')),
    path('gogogo/', include('gogogo.urls')),
    path('api/targets/', include('web_target.urls')),
    path('api/ranking/', include('ranking.urls')),
]
