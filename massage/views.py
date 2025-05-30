from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import datetime  
from datetime import datetime, timedelta 
import json
from .db import get_db_connection
from django.conf import settings
import jwt
from .db import get_db_connection

JWT_SECRET = settings.JWT_SECRET
JWT_EXPIRATION_SECONDS = 3600 * 24 * 7  # 7天


@csrf_exempt
@require_http_methods(["POST"])
def register_user(request):
    try:
        data = json.loads(request.body)
        # 获取用户信息
        user_name = data.get("user_name")
        phone_number = data.get("phone_number")
        avatar_url = data.get("avatar_url")
        department = data.get("department")
        pwd = data.get("pwd")
        age = data.get("age")
        height = data.get("height")
        # 必填字段校验
        if not user_name or not phone_number or not avatar_url or not department or not pwd or not age or not height:
            return JsonResponse({"error": "user_name and phone_number are required"}, status=400)
        # 连接数据库
        conn = get_db_connection()
        cursor = conn.cursor()

        # 插入用户数据
        sql = " INSERT INTO UserInfo (user_name, phone_number, avatar_url, department, pwd, age, height)  VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (user_name, phone_number,
                       avatar_url, department, pwd, age, height))
        conn.commit()

        # 获取新注册用户的 uid
        user_id = cursor.lastrowid

        return JsonResponse({"message": "User registered successfully", "uid": user_id}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone_number')
        pwd = data.get('pwd')

        if not phone or not pwd:
            return JsonResponse({"error": "phone and pwd are required"}, status=400)

        # 查询用户
        sql = "SELECT * FROM UserInfo WHERE phone_number = %s AND pwd = %s"
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (phone, pwd))
        user = cursor.fetchone()

        # 用户存在，生成 JWT token
        if user:
            token_payload = {'id': user['uid'], 'exp': datetime.utcnow(
            ) + timedelta(seconds=JWT_EXPIRATION_SECONDS)}
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
def user_info(request, item_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM UserInfo WHERE id = %s", (item_id,))
        user = cursor.fetchone()
        return JsonResponse({user: user, "message": "phone_number not exists"}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        cursor.close()
        conn.close()

@csrf_exempt 
def exercise_reminders(request, item_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ExerciseReminders WHERE uid = %s and is_active = true ORDER BY reminder_time ASC", (item_id,)) 
        list = cursor.fetchall()  # 获取所有匹配的记录（List[tuple]）

        if list:
            # 将查询结果（List[tuple]）转换为 List[dict]，方便 JSON 序列化
            columns = [desc[0] for desc in cursor.description]  # 获取列名
            exercise_list = [dict(zip(columns, row)) for row in list]  # 每行转为字典
            return JsonResponse({"data": exercise_list}, status=200)
        else:
            return JsonResponse({"message": "没有找到该用户的运动提醒记录"}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        cursor.close()
        conn.close()


@csrf_exempt
def check_phone(request, phone_number):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM UserInfo WHERE phone_number = %s", (phone_number,))
        if cursor.fetchone():
            return JsonResponse({"error": "phone_number already exists"}, status=400)
        return JsonResponse({"message": "phone_number not exists"}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def get_period_start_end(target_cycle):
    today = datetime.today().date()
    if target_cycle == 'day':
        start_date = end_date = today
    elif target_cycle == 'week':
        start_date = today - timedelta(days=today.weekday())  # 本周一
        end_date = start_date + timedelta(days=6)  # 本周日
    elif target_cycle == 'month':
        start_date = today.replace(day=1)  # 本月第一天
        if today.month == 12:
            next_month = today.replace(year=today.year+1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month+1, day=1)
        end_date = next_month - timedelta(days=1)
    else:
        start_date = end_date = today  # 默认日
    return start_date, end_date

def calculate_completion(target_type, target_value, actual_duration, actual_calorie):
    if target_type == '锻炼时长':
        return min(round((actual_duration / target_value) * 100, 2), 100)
    elif target_type == '燃烧卡路里':
        return min(round((actual_calorie / target_value) * 100, 2), 100)
    else:
        return 0

def get_weekly_stats(uid, conn):
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT DATE(record_time) AS record_date, SUM(duration) AS total_duration
        FROM ExerciseRecords
        WHERE uid = %s AND record_time BETWEEN %s AND %s AND is_deleted = 0 AND verification_status = 'pass'
        GROUP BY record_date
        ORDER BY record_date ASC
        """,
        (uid, start_of_week, end_of_week)
    )
    records = cursor.fetchall()
    daily_durations = []
    total_duration = 0
    for i in range(7):
        current_date = start_of_week + timedelta(days=i)
        daily_duration = next((rec[1] or 0 for rec in records if rec[0] == current_date), 0)
        daily_durations.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'weekday': current_date.strftime('%A'),
            'duration': daily_duration
        })
        total_duration += daily_duration
    avg_duration = round(total_duration / 7, 2) if total_duration > 0 else 0
    max_duration = max(d['duration'] for d in daily_durations)
    min_duration = min(d['duration'] for d in daily_durations if d['duration'] > 0) if total_duration > 0 else 0
    max_day = next((d['date'] for d in daily_durations if d['duration'] == max_duration), '-')
    min_day = next((d['date'] for d in daily_durations if d['duration'] == min_duration), '-')
    return {
        'total_duration': total_duration,
        'avg_duration': avg_duration,
        'max_duration': max_duration,
        'max_day': max_day,
        'min_duration': min_duration,
        'min_day': min_day,
        'daily_durations': daily_durations
    }

@csrf_exempt
def exercise_overview(request, uid):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 获取用户目标
        cursor.execute(
            """
            SELECT target_cycle, target_type, target_duration, target_calorie
            FROM ExerciseTargets
            WHERE uid = %s
            ORDER BY target_id DESC
            LIMIT 1
            """,
            (uid,)
        )
        target = cursor.fetchone()
        if not target:
            return JsonResponse({"error": "No target found for user"}, status=404)
        # target_cycle = request.GET.get('target_cycle', target[0])
        target_type, target_duration, target_calorie = target[1], target[2], target[3]
        target_value = target_duration or target_calorie or 1
        start_date, end_date = get_period_start_end(target[0])

        # 获取实际运动数据
        cursor.execute(
            """
            SELECT SUM(duration) AS total_duration, SUM(calorie) AS total_calorie
            FROM ExerciseRecords
            WHERE uid = %s AND record_time BETWEEN %s AND %s AND is_deleted = 0 AND verification_status = 'pass'
            """,
            (uid, start_date, end_date)
        )
        record = cursor.fetchone()
        total_duration = record[0] or 0
        total_calorie = record[1] or 0
        completion_percent = calculate_completion(target_type, target_value, total_duration, total_calorie)

        # 获取周统计数据
        weekly_stats = get_weekly_stats(uid, conn)

        return JsonResponse({
            "target_cycle": target[0],
            "target_type": target_type,
            "target_value": target_value,
            "actual_duration": total_duration,
            "actual_calorie": total_calorie,
            "completion_percent": completion_percent,
            "period_start": str(start_date),
            "period_end": str(end_date),
            "weekly_stats": weekly_stats
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
