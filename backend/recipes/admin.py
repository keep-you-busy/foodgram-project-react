from django.contrib import admin
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админ панель для модели Ингредиентов."""

    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


class IngredientRecipeInline(admin.TabularInline):
    """Форма для модели Ингредиентов, связзаной по первичному ключу."""

    model = IngredientRecipe
    extra = 1


class TagRecipeInline(admin.TabularInline):
    """Форма для модели Тега, связзаной по первичному ключу."""

    model = TagRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админ панель для модели Рецептов."""

    list_display = (
        'author',
        'name',
        'get_tags',
        'get_ingredients',
        'get_favorites'
    )
    search_fields = (
        'author__username',
        'name',
        'tags__name',
    )
    empty_value_display = '-пусто-'
    inlines = [IngredientRecipeInline, TagRecipeInline]

    def get_tags(self, recipe):
        return ', '.join(
            tag.name for tag in recipe.tags.all()
        )

    def get_ingredients(self, recipe):
        return ', '.join(
            ingredient.name for ingredient in recipe.ingredients.all()
        )

    def get_favorites(self, recipe):
        return recipe.in_favorites.count()

    get_tags.short_description = 'Теги'
    get_ingredients.short_description = 'Ингредиенты'
    get_favorites.short_description = 'В избранных'


admin.site.register(Tag)
