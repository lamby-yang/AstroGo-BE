from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import ExerciseRecords
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from web_profile.models import User
from django.db.models import Sum
from .serializers import ExerciseRecordSerializer
from rest_framework.decorators import api_view


@csrf_exempt  # 关闭CSRF验证（可以根据实际情况处理）
def submit_exercise_record(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # 获取POST请求中的JSON数据

            # 获取当前日期
            current_date = datetime.now().date()

            user_id = data.get('user_id')

            if not user_id:
                return JsonResponse({'code': 400, 'message': '用户ID不能为空'}, status=400)

            try:
    # 获取对应的 User 实例
                user = User.objects.get(uid=user_id)  # 假设 User 模型的主键字段是 id
            except User.DoesNotExist:
                return JsonResponse({'code': 404, 'message': '用户不存在'}, status=404)

            # 保存运动记录
            exercise_record = ExerciseRecords(
                uid=user,  # 用户ID，外键
                exercise_type=data.get('exercise_type'),
                duration=data.get('duration'),
                distance=data.get('distance'),
                calorie=data.get('calorie'),
                verification_photo_url=data.get('verification_photo_url'),
                verification_status='pending',  # 假设刚上传为待审核状态
                record_time=current_date,  # 运动时间（日期）
            )
            exercise_record.save()  # 保存记录

            return JsonResponse({'code': 200, 'message': 'Success'}, status=200)

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'code': 500, 'message': f'服务器错误: {str(e)}'}, status=500)

    return JsonResponse({'code': 400, 'message': '请求方法不支持'}, status=400)


# 获取当前用户的运动记录
def get_exercise_records(request):
    user_id = request.GET.get('uid')  # 从请求中获取用户ID
    
    records = ExerciseRecords.objects.filter(uid=user_id, is_deleted=False)

    # 将记录数据序列化为字典，返回给前端
    records_data = [{
        'record_id': record.record_id,
        'exercise_type': record.exercise_type,
        'duration': record.duration,
        'distance': record.distance,
        'calorie': record.calorie,
        'verification_photo_url': record.verification_photo_url,
        #'record_time': record.record_time.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化时间
    } for record in records]

    return JsonResponse({'data': records_data}, safe=False)


@api_view(['GET'])
def get_time_records(request):
    try:
        # 获取前端传来的参数
        uid = request.query_params.get('uid')
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        if not all([uid, start_time, end_time]):
            return Response(
                {"error": "uid, start_time and end_time are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 查询符合条件的运动记录
        records = ExerciseRecords.objects.filter(
            uid=uid,
            record_time__gte=start_time,
            record_time__lte=end_time,
            is_deleted=False
        ).values('exercise_type').annotate(
            total_duration=Sum('duration')
        )

        if not records.exists():
            return Response(
                {"code": 1, "msg": "No records found", "data": []},
                status=status.HTTP_200_OK
            )

        return Response({
            "code": 0,
            "msg": "success",
            "data": list(records)  # 转换为列表
        })

    except Exception as e:
        return Response(
            {"code": 500, "msg": f"Server error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    


class ExerciseRecordsByTimeRangeView(APIView):
    def get(self, request):
        # 获取前端传来的uid参数
        uid = request.query_params.get('uid')  # 获取传入的用户ID
        if not uid:
            return Response({"error": "uid is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取当前日期
        current_date = datetime.now().date()

        # 获取当前周的开始和结束日期
        start_of_week = current_date - timedelta(days=current_date.weekday()) #- timedelta(days=current_date.weekday())  # 当前周的周一
        end_of_week = start_of_week + timedelta(days=6)  # 当前周的周日

        # 查询符合条件的运动记录
        query = ExerciseRecords.objects.filter(
            uid=uid,  # 按用户ID过滤
            record_time__gte=start_of_week,  # 本周的开始时间
            record_time__lte=end_of_week,    # 本周的结束时间
            is_deleted=False  # 只查询未删除的记录
        ).values('exercise_type').annotate(
            total_duration=Sum('duration')  # 按运动类型汇总总时长
        )

        # 如果没有符合条件的记录
        if not query.exists():
            return Response({"message": "No records found for the specified user and week."}, status=status.HTTP_404_NOT_FOUND)

        # 返回查询到的数据
        return Response({
            "code": 0,
            "msg": "success",
            "data": query
        })
    
