from django.contrib import admin
from apps.user.models.user_model import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ["id", "phone_number", "date_joined"]
    search_fields = ["phone_number"]
    readonly_fields = ["password", "phone_number"]
