from rest_framework import serializers

from apps.habits.models import HabitLog


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = ("id", "date", "created_at")
        read_only_fields = ("created_at",)

    def validate(self, attrs: dict) -> dict:
        habit = self.context["habit"]
        date = attrs["date"]
        already_exists = HabitLog.objects.filter(habit=habit, date=date).exists()
        if already_exists:
            raise serializers.ValidationError(
                {"date": "Date with habit already exists"}
            )
        return attrs
