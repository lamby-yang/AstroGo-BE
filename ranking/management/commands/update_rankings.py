# ranking/management/commands/update_rankings.py
from django.core.management.base import BaseCommand
from django.db.models import Sum, F
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth
from ranking.models import ExerciseRecords, DailyRanking, WeeklyRanking, MonthlyRanking
from web_profile.models import User
from datetime import date, timedelta
from collections import defaultdict

class Command(BaseCommand):
    help = "Update daily, weekly, and monthly rankings for all users"

    def handle(self, *args, **kwargs):
        # 每日统计
        self.update_daily_rankings()

        # 每周统计
        self.update_weekly_rankings()

        # 每月统计
        self.update_monthly_rankings()

        self.stdout.write(self.style.SUCCESS('Successfully updated all rankings'))

    def update_daily_rankings(self):
        # 获取所有有记录的日期
        all_dates = ExerciseRecords.objects.dates('record_time', 'day').distinct()

        for record_date in all_dates:
            # 获取当天的所有记录，并关联 User 表获取 department
            daily_stats = ExerciseRecords.objects.filter(
                record_time=record_date
            ).select_related().extra(
                tables=['web_profile_user'],
                where=[
                    'web_profile_exerciserecords.uid = web_profile_user.uid'
                ]
            )  # 这种方法可能不适用于所有数据库

            # 更可靠的方法：在 Python 中处理关联
            daily_stats = []
            for record in ExerciseRecords.objects.filter(record_time=record_date):
                try:
                    user = User.objects.get(uid=record.uid)
                    daily_stats.append({
                        'uid': record.uid,
                        'department': user.department,
                        'calorie': record.calorie,
                        'duration': record.duration,
                    })
                except User.DoesNotExist:
                    continue

            # 按 UID 分组统计
            from collections import defaultdict
            uid_stats = defaultdict(lambda: {'total_duration': 0, 'total_calorie': 0.0})
            for stat in daily_stats:
                uid_stats[stat['uid']]['total_duration'] += stat['duration']
                uid_stats[stat['uid']]['total_calorie'] += stat['calorie']

            # 更新 DailyRanking
            for uid, stats in uid_stats.items():
                DailyRanking.objects.update_or_create(
                    uid=uid,
                    record_date=record_date,
                    defaults={
                        'total_duration': stats['total_duration'],
                        'total_calorie': stats['total_calorie'],
                    }
                )

    def update_weekly_rankings(self):
        # 获取所有有记录的周
        all_weeks = ExerciseRecords.objects.annotate(
            week_start=ExtractWeek('record_time'),
            year=ExtractYear('record_time')
        ).values('week_start', 'year').distinct()

        for week_data in all_weeks:
            week_start = self.get_week_start_date(week_data['week_start'], week_data['year'])
            end_date = week_start + timedelta(days=6)

            # 获取当周的所有记录，并关联 User 表获取 department
            weekly_stats = []
            for record in ExerciseRecords.objects.filter(
                record_time__gte=week_start,
                record_time__lte=end_date
            ):
                try:
                    user = User.objects.get(uid=record.uid)
                    weekly_stats.append({
                        'uid': record.uid,
                        'department': user.department,
                        'calorie': record.calorie,
                        'duration': record.duration,
                    })
                except User.DoesNotExist:
                    continue

            # 按 UID 分组统计
            uid_stats = defaultdict(lambda: {'total_duration': 0, 'total_calorie': 0.0})
            for stat in weekly_stats:
                uid_stats[stat['uid']]['total_duration'] += stat['duration']
                uid_stats[stat['uid']]['total_calorie'] += stat['calorie']

            # 更新 WeeklyRanking
            for uid, stats in uid_stats.items():
                WeeklyRanking.objects.update_or_create(
                    uid=uid,
                    week_start=week_start,
                    defaults={
                        'total_duration': stats['total_duration'],
                        'total_calorie': stats['total_calorie'],
                    }
                )

    def update_monthly_rankings(self):
        # 获取所有有记录的月
        all_months = ExerciseRecords.objects.annotate(
            month_start=ExtractMonth('record_time'),
            year=ExtractYear('record_time')
        ).values('month_start', 'year').distinct()

        for month_data in all_months:
            start_date = date(month_data['year'], month_data['month_start'], 1)
            if month_data['month_start'] == 12:
                end_date = date(month_data['year'] + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(month_data['year'], month_data['month_start'] + 1, 1) - timedelta(days=1)

            # 获取当月的所有记录，并关联 User 表获取 department
            monthly_stats = []
            for record in ExerciseRecords.objects.filter(
                record_time__gte=start_date,
                record_time__lte=end_date
            ):
                try:
                    user = User.objects.get(uid=record.uid)
                    monthly_stats.append({
                        'uid': record.uid,
                        'department': user.department,
                        'calorie': record.calorie,
                        'duration': record.duration,
                    })
                except User.DoesNotExist:
                    continue

            # 按 UID 分组统计
            uid_stats = defaultdict(lambda: {'total_duration': 0, 'total_calorie': 0.0})
            for stat in monthly_stats:
                uid_stats[stat['uid']]['total_duration'] += stat['duration']
                uid_stats[stat['uid']]['total_calorie'] += stat['calorie']

            # 更新 MonthlyRanking
            for uid, stats in uid_stats.items():
                MonthlyRanking.objects.update_or_create(
                    uid=uid,
                    month_start=start_date,
                    defaults={
                        'total_duration': stats['total_duration'],
                        'total_calorie': stats['total_calorie'],
                    }
                )

    def get_week_start_date(self, week_num, year):
        # 计算给定年份和周数的周开始日期（周一）
        from datetime import datetime, timedelta
        first_day = datetime(year, 1, 1)
        days_offset = (7 - first_day.weekday()) % 7  # 找到第一个周一
        first_monday = first_day + timedelta(days=days_offset)
        return first_monday + timedelta(weeks=week_num - 1)