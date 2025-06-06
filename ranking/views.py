# ranking/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth
from ranking.models import ExerciseRecords, DailyRanking, WeeklyRanking, MonthlyRanking
from web_profile.models import User
from datetime import date, timedelta
from collections import defaultdict
from .serializers import ExerciseRecordSerializer

class CampusRankingView(APIView):
    def get(self, request):
        period = request.query_params.get('period', 'daily')  # daily, weekly, monthly
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        try:
            if start_date_str:
                start_date = date.fromisoformat(start_date_str)
            else:
                start_date = None

            if end_date_str:
                end_date = date.fromisoformat(end_date_str)
            else:
                end_date = None
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # 获取符合条件的记录
        if period == 'daily':
            records = self.get_daily_records(start_date, end_date)
        elif period == 'weekly':
            records = self.get_weekly_records(start_date, end_date)
        elif period == 'monthly':
            records = self.get_monthly_records(start_date, end_date)
        else:
            return Response({"error": "Invalid period. Use daily, weekly, or monthly."}, status=status.HTTP_400_BAD_REQUEST)

        # 进一步过滤无效记录
        valid_records = []
        for record in records:
            if record.verification_status == 'pass' and record.is_deleted == 0:
                valid_records.append(record)

        # 按 uid 分组统计，并携带 department 和 user_name 信息
        uid_stats = defaultdict(lambda: {'total_calorie': 0, 'department': None, 'user_name': None,'avatar_url':None})
        for record in valid_records:
            try:
                user = User.objects.get(uid=record.uid)
                uid_stats[record.uid]['total_calorie'] += record.calorie
                # 确保 department 和 user_name 只设置一次（避免重复查询）
                if uid_stats[record.uid]['department'] is None:
                    uid_stats[record.uid]['department'] = user.department
                    uid_stats[record.uid]['user_name'] = user.user_name  # 新增字段
                    uid_stats[record.uid]['avatar_url'] = user.avatar_url # 新增字段
            except User.DoesNotExist:
                continue

        # 按卡路里从高到低排序
        sorted_uid_stats = sorted(uid_stats.items(), key=lambda x: x[1]['total_calorie'], reverse=True)

        # 转换为 API 响应格式
        data = []
        for uid, stats in sorted_uid_stats:
            data.append({
                "uid": uid,
                "user_name": stats['user_name'],
                "avatar_url": stats['avatar_url'],
                "department": stats['department'],
                "period": self.get_period_label(period, start_date, end_date),
                "total_calorie": stats['total_calorie'],
            })

        return Response(data)

    def get_daily_records(self, start_date, end_date):
        """获取指定日期范围内的记录"""
        query = ExerciseRecords.objects.all()
        if start_date:
            query = query.filter(record_time__gte=start_date)
        if end_date:
            query = query.filter(record_time__lte=end_date)
        return query

    def get_weekly_records(self, start_date, end_date):
        """获取指定周范围内的记录"""
        query = ExerciseRecords.objects.all()
        if start_date:
            query = query.filter(record_time__gte=start_date)
        if end_date:
            query = query.filter(record_time__lte=end_date)
        return query.annotate(
            week_start=ExtractWeek('record_time'),
            year=ExtractYear('record_time')
        ).values('week_start', 'year').annotate(
            total_calorie=Sum('calorie')
        )

    def get_monthly_records(self, start_date, end_date):
        """获取指定月范围内的记录"""
        query = ExerciseRecords.objects.all()
        if start_date:
            query = query.filter(record_time__gte=start_date)
        if end_date:
            query = query.filter(record_time__lte=end_date)
        return query.annotate(
            month_start=ExtractMonth('record_time'),
            year=ExtractYear('record_time')
        ).values('month_start', 'year').annotate(
            total_calorie=Sum('calorie')
        )

    def get_period_label(self, period, start_date, end_date):
        """生成周期标签"""
        if period == 'daily':
            if start_date and end_date:
                return f"{start_date}至{end_date}"
            elif start_date:
                return f"从{start_date}开始"
            elif end_date:
                return f"到{end_date}结束"
            else:
                return "所有日期"
        elif period == 'weekly':
            return "本周"
        elif period == 'monthly':
            return "本月"
        return "未知周期"


class ExerciseRecordsView(APIView):
    """
    特定用户的运动记录API视图
    GET: 获取特定用户的所有运动记录
    POST: 为特定用户创建新的运动记录
    """

    def get(self, request, uid):
        """获取特定用户的所有运动记录"""
        try:
            # 获取特定用户且未删除的记录
            records = ExerciseRecords.objects.filter(
                uid=uid,
                is_deleted=False
            ).order_by('-record_time')  # 按记录时间倒序排列

            serializer = ExerciseRecordSerializer(records, many=True)

            return Response({
                "code": 0,
                "msg": "success",
                "data": serializer.data
            })

        except Exception as e:
            return Response({
                "code": -1,
                "msg": f"获取记录失败: {str(e)}",
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, uid):
        """为特定用户创建新的运动记录"""
        try:
            # 将URL中的uid添加到请求数据中
            request_data = request.data.copy()
            request_data['uid'] = uid

            serializer = ExerciseRecordSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "code": 0,
                    "msg": "记录创建成功",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "code": -2,
                "msg": "数据验证失败",
                "errors": serializer.errors,
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "code": -1,
                "msg": f"创建记录失败: {str(e)}",
                "data": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExerciseRecordDetailView(APIView):
    """
    单条运动记录操作
    GET: 获取单条记录
    PUT: 更新单条记录
    DELETE: 删除记录（软删除）
    """

    def get_object(self, pk):
        try:
            return ExerciseRecords.objects.get(record_id=pk, is_deleted=False)
        except ExerciseRecords.DoesNotExist:
            return None

    def get(self, request, pk):
        """获取单条记录"""
        record = self.get_object(pk)
        if not record:
            return Response({
                "code": -3,
                "msg": "记录不存在或已删除",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ExerciseRecordSerializer(record)
        return Response({
            "code": 0,
            "msg": "success",
            "data": serializer.data
        })

    def put(self, request, pk):
        """更新单条记录"""
        record = self.get_object(pk)
        if not record:
            return Response({
                "code": -3,
                "msg": "记录不存在或已删除",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ExerciseRecordSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": 0,
                "msg": "记录更新成功",
                "data": serializer.data
            })

        return Response({
            "code": -2,
            "msg": "数据验证失败",
            "errors": serializer.errors,
            "data": None
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """软删除记录（标记is_deleted）"""
        record = self.get_object(pk)
        if not record:
            return Response({
                "code": -3,
                "msg": "记录不存在或已删除",
                "data": None
            }, status=status.HTTP_404_NOT_FOUND)

        # 软删除 - 标记为已删除
        record.is_deleted = True
        record.save()

        return Response({
            "code": 0,
            "msg": "记录已删除",
            "data": None
        }, status=status.HTTP_200_OK)