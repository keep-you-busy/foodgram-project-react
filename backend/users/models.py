from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models

from core.user_validation import check_username


USER_HELP_TEXT_TEMPLATE = 'Обязательно для заполнения, не более {} символов.'


class User(AbstractUser):
    """Модель пользователя."""

    username_validator = ASCIIUsernameValidator()

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text=(
            USER_HELP_TEXT_TEMPLATE.format(settings.EMAIL_FIELD_MAX_LENGHT)
        ),
        unique=True,
        blank=False,
        null=False

    )
    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        help_text=(
            USER_HELP_TEXT_TEMPLATE.format(settings.USER_FIELD_MAX_LENGHT)
        ),
        max_length=settings.USER_FIELD_MAX_LENGHT,
        unique=True,
        validators=[username_validator],
        blank=False,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        help_text=(
            USER_HELP_TEXT_TEMPLATE.format(settings.USER_FIELD_MAX_LENGHT)
        ),
        max_length=settings.USER_FIELD_MAX_LENGHT,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        help_text=(
            USER_HELP_TEXT_TEMPLATE.format(settings.USER_FIELD_MAX_LENGHT)
        ),
        max_length=settings.USER_FIELD_MAX_LENGHT,
        blank=False,
    )
    password = models.CharField(
        verbose_name='Пароль',
        help_text=(
            USER_HELP_TEXT_TEMPLATE.format(settings.USER_FIELD_MAX_LENGHT)
        ),
        max_length=settings.USER_FIELD_MAX_LENGHT,
        blank=False,
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'username', 'first_name', 'last_name', 'password'
    ]

    def clean(self):
        super().clean()
        check_username(value=self.username)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username


class Follow(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name="unique_follow"
            )
        ]

    def __str__(self) -> str:
        return f'{self.user.username}: {self.author.username}'
