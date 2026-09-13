from dataclasses import dataclass
from datetime import date, timedelta

from django.utils import timezone

from apps.habits.models import Habit
from apps.habits.repositories.habit_log import HabitLogRepository


@dataclass
class HabitStreakStats:
    current_streak: int
    longest_streak: int
    today_completed: bool
    is_at_risk: bool


def calculate_longest_streak(dates: set[date]) -> int:
    if not dates:
        return 0
    sorted_dates = sorted(dates)
    longest_streak = 1
    current_run = 1
    for i in range(1, len(sorted_dates)):
        if sorted_dates[i] - sorted_dates[i - 1] == timedelta(1):
            current_run += 1
        else:
            current_run = 1
        longest_streak = max(longest_streak, current_run)
    return longest_streak


def calculate_current_streak(dates: set[date]) -> int:
    today = timezone.localdate()
    check_date = today if today in dates else today - timedelta(days=1)

    streak = 0
    while check_date in dates:
        streak += 1
        check_date -= timedelta(days=1)
    return streak


class HabitLogService:
    def __init__(self, repo: HabitLogRepository):
        self.repo = repo

    def get_streak_stats(self, habit: Habit) -> HabitStreakStats:
        today = timezone.localdate()
        dates = self.repo.get_all_dates_for_habit(habit)
        current_streak = calculate_current_streak(dates)
        longest_streak = calculate_longest_streak(dates)
        today_completed = today in dates
        is_at_risk = not today_completed and current_streak > 0
        return HabitStreakStats(
            current_streak=current_streak,
            longest_streak=longest_streak,
            today_completed=today_completed,
            is_at_risk=is_at_risk,
        )
