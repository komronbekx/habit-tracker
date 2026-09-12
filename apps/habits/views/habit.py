from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.habits.models import Habit
from apps.habits.serializers import HabitSerializer


class HabitListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        habits = Habit.objects.filter(user=request.user)
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = HabitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HabitDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, habit_id: int, user) -> Habit:
        return get_object_or_404(Habit, id=habit_id, user=user)

    def get(self, request: Request, habit_id: int) -> Response:
        habit = self.get_object(habit_id, request.user)
        return Response(HabitSerializer(habit).data)

    def patch(self, request: Request, habit_id: int) -> Response:
        habit = self.get_object(habit_id, request.user)
        serializer = HabitSerializer(habit, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, habit_id: int) -> Response:
        habit = self.get_object(habit_id, request.user)
        habit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
