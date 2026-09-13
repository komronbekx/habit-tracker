from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Habit(models.Model):
    class Choices(models.TextChoices):
        DAILY = "daily", "Daily"

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="habits")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    frequency = models.CharField(
        max_length=50, choices=Choices.choices, default=Choices.DAILY
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "habit"
        verbose_name = "Habit"
        verbose_name_plural = "Habits"
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(fields=["user", "name"], name="unique_habit_user")
        ]
