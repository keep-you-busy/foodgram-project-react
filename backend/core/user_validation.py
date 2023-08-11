from rest_framework.exceptions import ValidationError


def check_username(value=None, username=None):
    """Декоратор валидирует значение поля username."""
    username = ['me'] if (username is None) else username
    username = [username.lower() for username in username]

    if value.lower() in username:
        raise ValidationError({f'{value}': 'Запрещенное имя пользователя!'})
