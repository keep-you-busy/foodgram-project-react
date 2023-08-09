from django.db import models
from users.models import User


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        verbose_name='Наименование тега',
        unique=True,
        max_length=250,
        blank=False,
    )
    color = models.CharField(
        verbose_name='Цвет тега',
        unique=True,
        max_length=7,
    )
    slug = models.SlugField(
        'slug',
        max_length=50,
        unique=True,
        blank=False,
        db_index=True
    )

    def __str__(self) -> str:
        return f'{self.name}'

class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        verbose_name='Наименование ингредиента',
        unique=True,
        max_length=250,
        blank=False,
    )
    measures = models.CharField(
        verbose_name='Единица измерения ингредиента',
        max_length=50,
        blank=False
    )

    def __str__(self) -> str:
        return f'{self.name}'

class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User, related_name='recipe',
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=0
    )
    name = models.CharField(
        verbose_name='Наименование рецепта',
        max_length=256,
        blank=False
    )
    image = models.ImageField(
        verbose_name='Изображение рецепта',
        upload_to='recipes/images/',
        null=False,
        blank=False,
        default=None
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        null=False,
        blank=False,
        default='Пустой текст'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты рецепта',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Теги рецепта',
    )
    cooking_time = models.DurationField(
        verbose_name='Время готовки рецепта',
        null=False,
        blank=False,
        default=0
    )

    def __str__(self) -> str:
        return f'{self.name}'

class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.PROTECT
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.DecimalField(
        verbose_name='Количество',
        max_digits=10,
        decimal_places=2,
        default=0

    )

    def __str__(self) -> str:
        return f'{self.ingredient} {self.recipe}'

class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тег',
        on_delete=models.PROTECT
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.tag} {self.recipe}'
