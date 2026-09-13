from drf_spectacular.utils import OpenApiParameter, extend_schema

from apps.habits.serializers import HabitLogSerializer

list_habit_logs_schema = extend_schema(
    summary="List logs for a habit",
    description="Returns all logs for the given habit, if it belongs to the authenticated user.",
    responses={200: HabitLogSerializer(many=True)},
    tags=["habit-logs"],
)

create_habit_log_schema = extend_schema(
    summary="Log a habit as completed",
    description=(
        "Creates a log entry for the given habit on the provided date. "
        "Fails if a log already exists for that habit and date."
    ),
    request=HabitLogSerializer,
    responses={201: HabitLogSerializer()},
    tags=["habit-logs"],
)

delete_habit_log_schema = extend_schema(
    summary="Delete a habit log",
    description="Deletes a specific log entry, if it belongs to the authenticated user's habit.",
    responses={204: None},
    tags=["habit-logs"],
)

get_habit_streak_schema = extend_schema(
    summary="Get streak statistics for a habit",
    description=(
        "Returns the current streak, longest streak, whether today is completed, "
        "and whether the streak is at risk."
    ),
    tags=["habit-stats"],
)

get_habit_monthly_stats_schema = extend_schema(
    summary="Get monthly statistics for a habit",
    description=(
        "Returns completion statistics for the given habit for a specific year and month."
    ),
    parameters=[
        OpenApiParameter(
            name="year",
            type=int,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Year to calculate statistics for, e.g. 2026.",
        ),
        OpenApiParameter(
            name="month",
            type=int,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Month to calculate statistics for (1-12).",
        ),
    ],
    tags=["habit-stats"],
)
