from django.db.models import Q
from django_filters import rest_framework as filters
from recipes.models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(
        method='get_filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_filter_is_in_shopping_cart'
    )
    author = filters.NumberFilter()
    tags = filters.CharFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
        )

    def get_filter_is_favorited(self, queryset, request, view):
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(in_favorites__user=self.request.user)
        return queryset

    def get_filter_is_in_shopping_cart(self, queryset, request, view):
        user = self.request.user
        if user.is_authenticated:
            return queryset.filter(in_carts__user=self.request.user)
        return queryset


class IngredientFilter(filters.FilterSet):
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
