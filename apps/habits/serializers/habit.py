from rest_framework import serializers

from apps.habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ("id", "name", "description", "frequency", "is_active", "created_at")
        read_only_fields = ("created_at",)
