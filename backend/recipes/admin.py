from django.contrib import admin
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe

admin.site.register(Ingredient)
admin.site.register(Tag)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1

class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'image',
        'text',
        'get_tags',
        'get_ingredients',
        'cooking_time'
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

    get_tags.short_description = 'Теги'
    get_ingredients.short_description = 'Ингредиенты'
