from typing import cast

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.habits.container import get_habit_log_repository
from apps.habits.models import Habit, HabitLog
from apps.habits.schemas.habit_log import (
    create_habit_log_schema,
    delete_habit_log_schema,
    list_habit_logs_schema,
)
from apps.habits.serializers import HabitLogSerializer


class HabitLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_habit(self, habit_id: int, user) -> Habit:
        return get_object_or_404(Habit, id=habit_id, user=user)

    @list_habit_logs_schema
    def get(self, request: Request, habit_id: int) -> Response:
        user = cast(User, request.user)
        habit = self.get_habit(habit_id, user)
        repo = get_habit_log_repository()
        logs = repo.get_logs_for_habit(habit)
        serializer = HabitLogSerializer(logs, many=True)
        return Response(serializer.data)

    @create_habit_log_schema
    def post(self, request: Request, habit_id: int) -> Response:
        user = cast(User, request.user)
        habit = self.get_habit(habit_id, user)
        serializer = HabitLogSerializer(data=request.data, context={"habit": habit})
        serializer.is_valid(raise_exception=True)
        serializer.save(habit=habit)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HabitLogDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_habit(self, habit_id: int, user) -> Habit:
        return get_object_or_404(Habit, id=habit_id, user=user)

    @delete_habit_log_schema
    def delete(self, request: Request, habit_id: int, log_id: int) -> Response:
        user = cast(User, request.user)
        habit = self.get_habit(habit_id, user)
        log = get_object_or_404(HabitLog, habit=habit, id=log_id)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
