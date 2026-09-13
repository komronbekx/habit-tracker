from django.urls import path

from apps.habits.views.habit import HabitDetailView, HabitListCreateView
from apps.habits.views.habit_log import HabitLogDeleteView, HabitLogListCreateView
from apps.habits.views.habit_streak import HabitMonthlyStatsView, HabitStreakView

urlpatterns = [
    path("", HabitListCreateView.as_view(), name="habit-list-create"),
    path("<int:habit_id>/", HabitDetailView.as_view(), name="habit-detail"),
    path(
        "<int:habit_id>/logs/", HabitLogListCreateView.as_view(), name="habit-log-list"
    ),
    path(
        "<int:habit_id>/logs/<int:log_id>/",
        HabitLogDeleteView.as_view(),
        name="habit-log-delete",
    ),
    path("<int:habit_id>/streak/", HabitStreakView.as_view(), name="habit-streak"),
    path(
        "<int:habit_id>/stats/",
        HabitMonthlyStatsView.as_view(),
        name="habit-monthly-stats",
    ),
]
