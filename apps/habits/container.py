from apps.habits.repositories.habit_log import HabitLogRepository
from apps.habits.services.stats_service import HabitMonthlyStatsService
from apps.habits.services.streak_service import HabitLogService


def get_habit_monthly_stats_service() -> HabitMonthlyStatsService:
    return HabitMonthlyStatsService(repo=HabitLogRepository())


def get_habit_log_repository() -> HabitLogRepository:
    return HabitLogRepository()


def get_habit_log_service() -> HabitLogService:
    return HabitLogService(repo=get_habit_log_repository())
