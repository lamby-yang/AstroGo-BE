import json
import uuid
import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import jwt
import requests
from .db import get_db_connection

JWT_SECRET = settings.JWT_SECRET
JWT_EXPIRATION_SECONDS = 3600 * 24 * 7  # 7天
# WECHAT_APP_ID = 'your_wechat_app_id'
# WECHAT_APP_SECRET = 'your_wechat_app_secret'


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    try:
        data = json.loads(request.body)
        user_type = data.get('type')
        sql = 'SELECT * FROM UserInfo'
        params = []

        # 账号密码登录
        if user_type == 1:
            phone = data.get('phone')
            pwd = data.get('pwd')
            if not phone or not pwd:
                return JsonResponse({"error": "phone and password are required"}, status=400)
            sql += " WHERE phone_number = %s AND pwd = %s"
            params.extend([phone, pwd])

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, params)
            user = cursor.fetchone()
        else:
            return JsonResponse({"error": "Only account/password login is supported"}, status=400)

        # 用户存在，生成 JWT token
        if user:
            token_payload = {
                'id': user['id'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRATION_SECONDS)
            }
            token = jwt.encode(token_payload, JWT_SECRET, algorithm='HS256')
            return JsonResponse({"token": token, "message": "Login successful"}, status=200)

        # 用户不存在
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()



@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    try:
        data = json.loads(request.body)

        # 手机号+密码注册
        user_name = data.get("user_name")
        phone_number = data.get("phone_number")
        avatar_url = data.get("avatar_url")
        department = data.get("department")
        pwd = data.get("pwd")
        age = data.get("age")
        height = data.get("height")
        weight = data.get("weight")
        create_time = datetime.datetime.now()

        if not user_name or not phone_number or not pwd:
            return JsonResponse({"error": "user_name, phone_number, and pwd are required"}, status=400)

        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO UserInfo (user_name, phone_number, avatar_url, department, pwd, age, height, weight, create_time) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (user_name, phone_number, avatar_url, department, pwd, age, height, weight, create_time))
        conn.commit()
        user_id = cursor.lastrowid

        return JsonResponse({"message": "User registered successfully", "uid": user_id}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
