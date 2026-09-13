from drf_spectacular.utils import extend_schema

from apps.habits.serializers import HabitSerializer

list_habits_schema = extend_schema(
    summary="List user's habits",
    description="Returns all habits belonging to the authenticated user.",
    responses={200: HabitSerializer(many=True)},
    tags=["habits"],
)

create_habit_schema = extend_schema(
    summary="Create a habit",
    description="Creates a new habit for the authenticated user.",
    request=HabitSerializer,
    responses={201: HabitSerializer()},
    tags=["habits"],
)

get_habit_schema = extend_schema(
    summary="Get a habit",
    description="Returns a single habit by id, if it belongs to the authenticated user.",
    responses={200: HabitSerializer()},
    tags=["habits"],
)

update_habit_schema = extend_schema(
    summary="Update a habit",
    description="Partially updates a habit by id, if it belongs to the authenticated user.",
    request=HabitSerializer,
    responses={200: HabitSerializer()},
    tags=["habits"],
)

delete_habit_schema = extend_schema(
    summary="Delete a habit",
    description="Deletes a habit by id, if it belongs to the authenticated user.",
    responses={204: None},
    tags=["habits"],
)