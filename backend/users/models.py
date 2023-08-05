from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models


class User(AbstractUser):
    "Модель пользователя."
    username_validator = ASCIIUsernameValidator()

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        help_text=('Обязательно для заполнения, не более 254 символа.'),
        unique=True,
        blank=False,
        null=False

    )
    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        help_text=('Обазятельно для заполнения, не более 150 символов.'),
        max_length=150,
        unique=True,
        validators=[username_validator],
        blank=False,
        null=False
    )
    first_name = models.CharField(
        verbose_name='Имя',
        help_text=('Обазятельно для заполнения, не более 150 символов.'),
        max_length=150,
        blank=False,
        null=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        help_text=('Обазятельно для заполнения, не более 150 символов.'),
        max_length=150,
        blank=False,
        null=False
    )
    password = models.CharField(
        verbose_name='Пароль',
        help_text=('Обазятельно для заполнения, не более 150 символов.'),
        max_length=150,
        blank=False,
        null=False
    )

    REQUIRED_FIELDS = [
        'email', 'first_name', 'last_name', 'password'
    ]

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи',
