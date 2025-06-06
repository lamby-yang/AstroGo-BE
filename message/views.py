from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta, date
import json
import jwt
from django.conf import settings
from django.db.models import Sum
from web_profile.models import User as UserInfo
from .models import ExerciseReminders, ExerciseTargets, ExerciseRecords

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
        required_fields = ["user_name", "phone_number", "avatar_url", "department", "pwd", "age", "height"]
        if not all(data.get(field) for field in required_fields):
            return JsonResponse({"error": "所有字段都是必填项"}, status=400)

        # 检查手机号是否已存在
        if UserInfo.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({"error": "手机号已被注册"}, status=400)

        # 创建用户
        user = UserInfo.objects.create(
            user_name=user_name,
            phone_number=phone_number,
            avatar_url=avatar_url,
            department=department,
            pwd=pwd,
            age=age,
            height=height
        )

        return JsonResponse({"message": "用户注册成功", "uid": user.uid}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    try:
        data = json.loads(request.body)
        phone = data.get('phone_number')
        pwd = data.get('pwd')

        if not phone or not pwd:
            return JsonResponse({"error": "手机号和密码是必填项"}, status=400)

        # 验证用户
        user = UserInfo.objects.filter(phone_number=phone, pwd=pwd).first()

        if user:
            token_payload = {'id': user.uid, 'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_SECONDS)}
            token = jwt.encode(token_payload, JWT_SECRET, algorithm='HS256')
            return JsonResponse({"token": token, "message": "登录成功", "uid": user.uid}, status=200)

        return JsonResponse({"error": "账号或密码错误"}, status=401)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def user_info(request, uid):
    try:
        user = UserInfo.objects.filter(uid=uid).first()
        if user:
            return JsonResponse({
                "user_name": user.user_name,
                "phone_number": user.phone_number,
                "avatar_url": user.avatar_url,
                "department": user.department,
                "age": user.age,
                "height": user.height
            }, status=200)
        return JsonResponse({"error": "用户不存在"}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def exercise_reminders(request, uid):
    try:
        reminders = ExerciseReminders.objects.filter(
            uid=uid,
            is_active=True
        ).order_by('reminder_time')

        if reminders.exists():
            reminder_list = [
                {
                    "reminder_id": r.reminder_id,
                    "reminder_time": r.reminder_time.strftime("%H:%M:%S"),
                    "is_active": r.is_active
                } for r in reminders
            ]
            return JsonResponse({"data": reminder_list}, status=200)
        else:
            return JsonResponse({"message": "没有找到该用户的运动提醒记录"}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def check_phone(request, phone_number):
    try:
        if UserInfo.objects.filter(phone_number=phone_number).exists():
            return JsonResponse({"error": "手机号已被注册"}, status=400)
        return JsonResponse({"message": "手机号可用"}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_period_start_end(target_cycle):
    today = date.today()
    if target_cycle == 'day':
        return today, today
    elif target_cycle == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        return start_date, end_date
    elif target_cycle == 'month':
        start_date = today.replace(day=1)
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        return start_date, end_date
    return today, today


def calculate_completion(target_type, target_value, actual_duration, actual_calorie):
    if target_type == '锻炼时长' and target_value > 0:
        return min(round((actual_duration / target_value) * 100, 2), 100)
    elif target_type == '燃烧卡路里' and target_value > 0:
        return min(round((actual_calorie / target_value) * 100, 2), 100)
    return 0


def get_weekly_stats(uid):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # 按天分组统计运动时长
    records = ExerciseRecords.objects.filter(
        uid=uid,
        record_time__date__range=[start_of_week, end_of_week],
        is_deleted=False,
        verification_status='pass'
    ).values('record_time__date').annotate(
        total_duration=Sum('duration')
    ).order_by('record_time__date')

    # 创建完整一周的数据
    daily_durations = []
    total_duration = 0

    for i in range(7):
        current_date = start_of_week + timedelta(days=i)
        duration_value = 0

        # 查找当天的记录
        for record in records:
            if record['record_time__date'] == current_date:
                duration_value = record['total_duration'] or 0
                break

        daily_durations.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'weekday': current_date.strftime('%A'),
            'duration': duration_value
        })
        total_duration += duration_value

    # 计算统计数据
    durations = [d['duration'] for d in daily_durations]
    max_duration = max(durations)
    min_duration = min(durations) if any(durations) else 0

    max_day = next((d['date'] for d in daily_durations if d['duration'] == max_duration),
                   None) if max_duration > 0 else None
    min_day = next((d['date'] for d in daily_durations if d['duration'] == min_duration),
                   None) if min_duration > 0 else None

    return {
        'total_duration': total_duration,
        'avg_duration': round(total_duration / 7, 2) if total_duration > 0 else 0,
        'max_duration': max_duration,
        'max_day': max_day or '-',
        'min_duration': min_duration,
        'min_day': min_day or '-',
        'daily_durations': daily_durations
    }


@csrf_exempt
def exercise_overview(request, uid):
    try:
        # 获取最新的运动目标
        target = ExerciseTargets.objects.filter(uid=uid).order_by('-target_id').first()

        if not target:
            return JsonResponse({"error": "未找到用户的运动目标"}, status=404)

        # 获取当前周期的起止日期
        start_date, end_date = get_period_start_end(target.target_cycle)

        # 查询当前周期内的运动记录
        records = ExerciseRecords.objects.filter(
            uid=uid,
            record_time__date__range=[start_date, end_date],
            is_deleted=False,
            verification_status='pass'
        ).aggregate(
            total_duration=Sum('duration'),
            total_calorie=Sum('calorie')
        )

        total_duration = records['total_duration'] or 0
        total_calorie = records['total_calorie'] or 0

        # 判断目标类型并计算完成度
        target_value = target.target_duration if target.target_type == '锻炼时长' else target.target_calorie
        completion_percent = calculate_completion(
            target.target_type,
            target_value or 0,
            total_duration,
            total_calorie
        )

        # 获取周统计数据
        weekly_stats = get_weekly_stats(uid)

        return JsonResponse({
            "target_cycle": target.target_cycle,
            "target_type": target.target_type,
            "target_value": target_value,
            "actual_duration": total_duration,
            "actual_calorie": total_calorie,
            "completion_percent": completion_percent,
            "period_start": start_date.strftime('%Y-%m-%d'),
            "period_end": end_date.strftime('%Y-%m-%d'),
            "weekly_stats": weekly_stats
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)