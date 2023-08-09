from django.contrib import admin
from recipes.models import Ingredient, Recipe, Tag

admin.site.register(Ingredient)
admin.site.register(Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'image',
        'text',
        'get_tags',
        'get_ingretients',
        'cooking_time'
    )
    empty_value_display = '-пусто-'

    def get_tags(self, recipe):
        return ', '.join(
            tag.name for tag in recipe.tags.all()
        )
    
    def get_ingretients(self, recipe):
        return ', '.join(
            ingredient.name for ingredient in recipe.ingredients.all()
        )

    get_tags.short_description = 'Теги'
    get_ingretients.short_description = 'Ингредиенты'
