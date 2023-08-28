from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админ панель для модели Пользователей."""

    list_display = (
        'email',
        'username',
    )
    search_fields = (
        'email',
        'username',
    )
    empty_value_display = '-пусто-'
