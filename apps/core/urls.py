from django.urls import include, path

urlpatterns = [
    path("habits/", include("apps.habits.urls")),
]
