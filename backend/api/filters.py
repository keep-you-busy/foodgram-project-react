from django.db.models import Q
from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    """Фильтр для модели рецепта."""

    is_favorited = filters.BooleanFilter(
        method='get_filter_by_relationship',
        field_name='in_favorites__user'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_filter_by_relationship',
        field_name='in_carts__user'
    )
    author = filters.NumberFilter()
    tags = filters.CharFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
        )

    def get_filter_by_relationship(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            filter_parameters = {name: user}
            return queryset.filter(
                Q(**filter_parameters) if value else ~Q(**filter_parameters)
            )
        return queryset


class IngredientFilter(filters.FilterSet):
    """Фильтр для модели Ингредиента.

    Даёт возможность фильра ингредиента по началу вхождения
    и в произвольном месте.
    """

    name = filters.CharFilter(method='filter_name')

    class Meta:
        model = Ingredient
        fields = (
            'name',
        )

    def filter_name(self, queryset, name, value):
        starts_with_queryset = queryset.filter(name__startswith=value)
        contains_queryset = queryset.filter(name__contains=value)

        sorted_queryset = starts_with_queryset.union(contains_queryset)
        return sorted_queryset
