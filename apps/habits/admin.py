from django.contrib import admin

from .models import Habit, HabitLog


class HabitLogInline(admin.TabularInline):
    model = HabitLog
    extra = 0
    fields = ("date", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("-date",)

    def get_queryset(self, request):
        # Faqat so'nggi 30 ta yozuvni ko'rsatamiz, sahifani yengil saqlash uchun
        qs = super().get_queryset(request)
        recent_ids = qs.order_by("-date").values_list("id", flat=True)[:30]
        return qs.filter(id__in=list(recent_ids))


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "frequency", "is_active", "created_at")
    list_filter = ("frequency", "is_active", "created_at")
    search_fields = ("name", "user__username")
    inlines = [HabitLogInline]


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ("habit", "date", "created_at")
    list_filter = ("date",)
    search_fields = ("habit__name",)
