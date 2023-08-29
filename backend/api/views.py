import tempfile

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (
    CartSerializer,
    CustomUserSerializer,
    FavoriteSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    ResponseFavoriteSerializer,
    ResponseSubscribeSerializer,
    TagSerializer
)
from core.action_method import save_delete_action
from core.creation_pdf import make_shopping_cart
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.http import urlquote
from django_filters import rest_framework as filters
from djoser.conf import settings
from djoser.views import UserViewSet
from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from users.models import Follow, User


class CustomUserViewSet(UserViewSet):
    """Взаимодействие с пользователями.

    Viewset позволяет создавать, изменять пользователя.
    Доступны методы подписки и вывода текущих подписок.
    """

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """Выдаёт разрешение на вывод данных рецепта по ключу."""
        if self.action == "retrieve":
            self.permission_classes = settings.PERMISSIONS.user_list
        return super().get_permissions()

    @action(
            methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,),
            url_path='subscribe',
            url_name='subscribe'
    )
    def subscribe(self, request, id):
        """Метод подписки пользователя на автора."""
        user = request.user
        author = get_object_or_404(User, pk=id)
        user_author = Follow.objects.filter(user=user, author=author)
        data_to_response = {
            'user': user.id,
            'author': author.id
        }
        return save_delete_action(
            request=request,
            objects=user_author,
            target=author,
            serializer_class=FollowSerializer,
            response_serializer_class=ResponseSubscribeSerializer,
            data=data_to_response
        )

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        url_path='subscriptions',
        url_name='subscriptions'
    )
    def subscriptions(self, request):
        """Метод вывода текущих подписок пользователя."""
        queryset = User.objects.filter(following__user=request.user)
        data = self.paginate_queryset(queryset=queryset)
        recipes_limit = request.query_params.get(
            self.paginator.recipes_limit_query_param
            )
        serializer = ResponseSubscribeSerializer(
            many=True,
            data=data,
            context={'request': request, 'recipes_limit': recipes_limit})
        serializer.is_valid()
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """Взаимодействие с тегами.

    Viewset позволяет выводить список тегов.
    Доступна возможность просмотра тега по ключу.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """Взаимодействие с ингредиентами.

    Viewset позволяет выводить список ингредиентов.
    Доступна возможность просмотра ингредиента по ключу,
    поиска ингредиента по входному значению.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Взаимодействие с рецептами.

    Viewset позволяет выводить список рецептов.
    Доступна возможность просмотра рецепта по ключу.
    Для авторизированных доступная возможность добавить
    рецепт в избранное, добавить рецепт в список покупок,
    скачать имеющийся список покупок.
    """

    queryset = Recipe.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        """Выдаёт разрешение на редактирование рецепта."""
        method = self.request.method
        if method == 'PATCH':
            self.permission_classes = (IsOwnerOrReadOnly,)
        return super().get_permissions()

    def get_serializer_class(self):
        """Определяет сериалайзер на основании метода запроса."""
        method = self.request.method
        if method in SAFE_METHODS:
            self.serializer_class = RecipeSerializer
        elif method == 'POST':
            self.serializer_class = RecipeCreateSerializer
            self.pagination_class = None
        elif method == 'PATCH':
            self.serializer_class = RecipeCreateSerializer
            self.pagination_class = None
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    @action(
            methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,),
            url_path='favorite',
            url_name='favorite'
    )
    def favorite(self, request, pk):
        """Метод для добавления рецепта в избранное."""
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        user_recipe = Favorite.objects.filter(user=user, recipe=recipe)
        data_to_response = {
            'user': user.id,
            'recipe': recipe.id
        }
        return save_delete_action(
            request=request,
            objects=user_recipe,
            target=recipe,
            serializer_class=FavoriteSerializer,
            response_serializer_class=ResponseFavoriteSerializer,
            data=data_to_response
        )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
        url_path='shopping_cart',
        url_name='shopping_cart'
    )
    def shopping_cart(self, request, pk):
        """Метод для добавления рецепта в список покупок."""
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        user_recipe = Cart.objects.filter(user=user, recipe=recipe)
        data_to_response = {
            'user': user.id,
            'recipe': recipe.id
        }
        return save_delete_action(
            request=request,
            objects=user_recipe,
            target=recipe,
            serializer_class=CartSerializer,
            response_serializer_class=ResponseFavoriteSerializer,
            data=data_to_response
        )

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        url_path='download_shopping_cart',
        url_name='download_shopping_cart'
    )
    def download_shopping_cart(self, request):
        """Метод для загрузки списка покупок в PDF формате."""
        with tempfile.NamedTemporaryFile(delete=False) as temp_pdf_file:
            temp_filename = temp_pdf_file.name

        make_shopping_cart(request.user, temp_filename)

        with open(temp_filename, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        response = HttpResponse(pdf_content, content_type='application/pdf')
        filename = urlquote(f"shopping_list_{request.user}.pdf")
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
