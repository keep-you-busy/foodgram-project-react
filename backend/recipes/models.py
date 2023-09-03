from colorfield.fields import ColorField
from django.conf import settings
from django.db import models

from users.models import User


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        verbose_name='Наименование тега',
        unique=True,
        max_length=settings.NAME_MAX_LENGHT,
        blank=False,
    )
    color = ColorField(
        verbose_name='Цвет тега',
        unique=True,
    )
    slug = models.SlugField(
        'slug',
        max_length=settings.SHORT_FIELD_MAX_LENGHT,
        unique=True,
        blank=False,
        db_index=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return f'{self.name}'


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        verbose_name='Наименование ингредиента',
        unique=True,
        max_length=settings.NAME_MAX_LENGHT,
        blank=False,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения ингредиента',
        max_length=settings.SHORT_FIELD_MAX_LENGHT,
        blank=False
    )

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient_with_unit'
            )
        ]

    def __str__(self) -> str:
        return f'{self.name}'


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=0,
    )
    name = models.CharField(
        verbose_name='Наименование рецепта',
        max_length=settings.RECIPE_NAME_MAX_LENGHT,
        blank=False,
        unique=True
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
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты рецепта',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Теги рецепта',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки рецепта',
        null=False,
        blank=False,
        default=1,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return f'{self.name}'


class IngredientRecipe(models.Model):
    """Промежуточная сущность между моделями рецептов и ингредиентов."""

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.PROTECT
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        null=False,
        blank=False,
        default=1

    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_with_recipe'
            )
        ]

    def __str__(self) -> str:
        return f'{self.ingredient}: {self.recipe}'


class TagRecipe(models.Model):
    """Промежуточная сущность между моделями рецептов и тегов."""

    tag = models.ForeignKey(
        Tag,
        verbose_name='Тег',
        on_delete=models.PROTECT
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f'{self.tag}: {self.recipe}'


class BaseListModel(models.Model):
    """Базовая модель для привязки пользователя и рецепта."""

    @staticmethod
    def get_user_related_name():
        return '%(class)ss'

    @staticmethod
    def get_recipe_related_name():
        return 'in_%(class)ss'

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name=get_user_related_name.__func__(),
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name=get_recipe_related_name.__func__(),
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.user.username}: {self.recipe.name}'


class Favorite(BaseListModel):
    """Модель избранных рецептов."""

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorites'
            )
        ]


class Cart(BaseListModel):
    """Модель списка покупок."""

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_cart'
            )
        ]
