from django.contrib import admin

from .models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "user_type",
        "is_active",
        "is_staff",
        "created_at",
    )
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("user_type", "is_active", "is_staff", "created_at")
