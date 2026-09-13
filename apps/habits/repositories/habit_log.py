from datetime import date

from django.db.models.query import QuerySet

from apps.habits.models import Habit, HabitLog


class HabitLogRepository:
    def get_logs_for_habit(
        self, habit: Habit, date_from: date | None = None, date_to: date | None = None
    ) -> QuerySet[HabitLog]:
        qs = HabitLog.objects.filter(habit=habit)
        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        return qs.order_by("date")

    def get_all_dates_for_habit(self, habit: Habit) -> set[date]:
        dates = HabitLog.objects.filter(habit=habit).values_list("date", flat=True)
        return set(dates)
