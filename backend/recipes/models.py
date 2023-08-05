from django.db import models
from users.models import User


class Recipe(models.Model):
    "Модель рецепта."

    author = models.ForeignKey(
        User, related_name='recipe',
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    ),
    name = models.CharField(
        verbose_name='Наименование рецепта',
        null=False,
        blank=False
    )
    image = models.ImageField(
        verbose_name='Изображение рецепта',
        upload_to='recipes/images/',
        null=False,
        blank=False,
        default=None
    ),
    text = models.TextField(
        verbose_name='Описание рецепта',
        null=False,
        blank=False
    ),
    ingredients = models.ManyToManyField(
        # Ingredient, - end the class for ingredient
        verbose_name='Ингредиенты рецепта',
        # choices = 
        null=False,
        blank=False
    ),
    tags = models.ManyToManyField(
        # Tags, - end the class fo tags
        verbose_name='Теги рецепта',
        # choices = 
        null=False,
        blank=False
    ),
    cooking_time = models.DurationField(
        verbose_name='Время готовки рецепта',
        null=False,
        blank=False
    )

class Tag(models.Model):
    "Модель тега."

    name = models.CharField(
        verbose_name='Наименование тега',
        unique=True,
        null=False,
        blank=False
    ),
    color = models.CharField(
        verbose_name='Цвет тега',
        max_length=16
    ),
    slug = models.SlugField(
        'slug',
        max_length=50,
        unique=True,
        blank=False,
        db_index=True
    )

class Ingredient(models.Model):
    "Модель ингредиента."

    name = models.CharField(
        verbose_name='Наименование ингредиента',
        unique=True,
        null=False,
        blank=False
    ),
    count = models.IntegerField(
        verbose_name='Количество ингредиента',
        null=False,
        blank=False
    )
    measures = models.CharField(
        verbose_name='Единица измерения ингредиента',
        null=False,
        blank=False
    )
