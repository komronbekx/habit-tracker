from drf_spectacular.utils import extend_schema

from apps.users.serializers import RegisterSerializer, TokenPairSerializer

register_schema = extend_schema(
    summary="Register a new user",
    description=(
        "Creates a new user account and returns JWT access and refresh tokens, "
        "logging the user in immediately."
    ),
    request=RegisterSerializer,
    responses={201: TokenPairSerializer()},
    tags=["users"],
)
