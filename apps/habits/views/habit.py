from typing import cast

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.habits.models import Habit
from apps.habits.schemas.habit import list_habits_schema, create_habit_schema, get_habit_schema, update_habit_schema, \
    delete_habit_schema
from apps.habits.serializers import HabitSerializer


class HabitListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @list_habits_schema
    def get(self, request: Request) -> Response:
        user = cast(User, request.user)
        habits = Habit.objects.filter(user=user)
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data)

    @create_habit_schema
    def post(self, request: Request) -> Response:
        user = cast(User, request.user)
        serializer = HabitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HabitDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, habit_id: int, user) -> Habit:
        return get_object_or_404(Habit, id=habit_id, user=user)

    @get_habit_schema
    def get(self, request: Request, habit_id: int) -> Response:
        user = cast(User, request.user)
        habit = self.get_object(habit_id, user)
        return Response(HabitSerializer(habit).data)

    @update_habit_schema
    def patch(self, request: Request, habit_id: int) -> Response:
        user = cast(User, request.user)
        habit = self.get_object(habit_id, user)
        serializer = HabitSerializer(habit, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @delete_habit_schema
    def delete(self, request: Request, habit_id: int) -> Response:
        user = cast(User, request.user)
        habit = self.get_object(habit_id, user)
        habit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
