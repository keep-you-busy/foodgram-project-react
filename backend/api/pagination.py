from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Пагинация с дополнительным параметром лимита рецептов."""

    page_size_query_param = 'limit'
    recipes_limit_query_param = 'recipes_limit'
