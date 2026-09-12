from dataclasses import asdict
from typing import cast

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.habits.container import get_habit_log_service, get_habit_monthly_stats_service
from apps.habits.models import Habit


class HabitStreakView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, habit_id: int, user) -> Habit:
        return get_object_or_404(Habit, id=habit_id, user=user)

    def get(self, request: Request, habit_id: int) -> Response:
        user = cast(User, request.user)
        habit = self.get_object(habit_id, user)
        service = get_habit_log_service()
        stats = service.get_streak_stats(habit)
        data = asdict(stats)
        return Response(data, status=status.HTTP_200_OK)


class HabitMonthlyStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, habit_id: int, user) -> Habit:
        return get_object_or_404(Habit, id=habit_id, user=user)

    def get(self, request: Request, habit_id: int) -> Response:
        user = cast(User, request.user)
        habit = self.get_object(habit_id, user)
        try:
            year = int(request.query_params.get("year", ""))
            month = int(request.query_params.get("month", ""))
        except (TypeError, ValueError):
            return Response(
                {
                    "detail": "year and month query parameters are required and must be integers."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        service = get_habit_monthly_stats_service()
        stats = service.calculate_monthly_stats(habit, year, month)
        data = asdict(stats)
        return Response(data, status=status.HTTP_200_OK)
