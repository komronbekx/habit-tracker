import calendar
from dataclasses import dataclass
from datetime import date

from django.utils import timezone

from apps.habits.models import Habit
from apps.habits.repositories.habit_log import HabitLogRepository


@dataclass
class HabitMonthlyStats:
    year: int
    month: int
    days_elapsed: int
    days_completed: int
    completion_percentage: float
    is_current_month: bool


class HabitMonthlyStatsService:
    def __init__(self, repo: HabitLogRepository):
        self.repo = repo

    def calculate_monthly_stats(
        self, habit: Habit, year: int, month: int
    ) -> HabitMonthlyStats:
        today = timezone.localdate()
        is_current_month = today.year == year and today.month == month
        if is_current_month:
            range_end = today
        else:
            _, last_day = calendar.monthrange(year, month)
            range_end = date(year, month, last_day)

        month_started = date(year, month, 1)
        habit_created = habit.created_at.date()
        range_start = max(month_started, habit_created)
        days_elapsed = (range_end - range_start).days + 1

        logs = self.repo.get_logs_for_habit(
            habit, date_from=range_start, date_to=range_end
        )
        days_completed = logs.count()

        if days_elapsed == 0:
            completion_percentage = 0.0
        else:
            completion_percentage = round((days_completed / days_elapsed) * 100, 2)

        return HabitMonthlyStats(
            year=year,
            month=month,
            days_elapsed=days_elapsed,
            days_completed=days_completed,
            completion_percentage=completion_percentage,
            is_current_month=is_current_month,
        )

    def calculate_overall_completion_rate(self, habit: Habit) -> float:
        today = timezone.localdate()
        habit_created = habit.created_at.date()

        days_elapsed = (today - habit_created).days + 1

        logs = self.repo.get_logs_for_habit(
            habit, date_from=habit_created, date_to=today
        )
        days_completed = logs.count()

        if days_elapsed == 0:
            return 0.0

        return round((days_completed / days_elapsed) * 100, 2)
