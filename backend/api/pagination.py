from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Пагинация с дополнительным параметром лимита рецептов."""

    page_size_query_param = 'limit'
    recipes_limit_query_param = 'recipes_limit'

    def paginate_queryset(self, queryset, request, view=None):
        self.recipes_limit = request.query_params.get(
            self.recipes_limit_query_param)
        return super().paginate_queryset(queryset, request, view)
