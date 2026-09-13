from django.db import models
from django.db.models import UniqueConstraint

from apps.habits.models import Habit


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.habit} - {self.date}"

    class Meta:
        db_table = "habit_log"
        verbose_name = "Habit log"
        verbose_name_plural = "Habit logs"
        constraints = [
            UniqueConstraint(fields=["habit", "date"], name="unique_habit_log")
        ]
