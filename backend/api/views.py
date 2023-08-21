from api.serializers import (CustomUserSerializer, FavoritesSerializer,
                             FollowSerializer, IngredientSerializer,
                             RecipeCreateSerializer, RecipeSerializer,
                             ResponseFavoritesSerializer,
                             ResponsesubscribeSerializer, TagSerializer)
from core.action_method import check_objects, save_delete_action, save_objects
from core.exceptions import ObjectExistsError, ObjectNotFoundError
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import Favorites, Ingredient, Recipe, Tag
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from users.models import Follow, User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    @action(
            methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=(permissions.IsAuthenticated,),
            url_path='subscribe',
            url_name='subscribe'
    )
    def subscribe(self, request, id):
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
            response_serializer_class=ResponsesubscribeSerializer,
            data=data_to_response
        )

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            self.serializer_class = RecipeSerializer
        else:
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
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        user_recipe = Favorites.objects.filter(user=user, recipe=recipe)
        data_to_response = {
            'user': user.id,
            'recipe': recipe.id
        }
        return save_delete_action(
            request=request,
            objects=user_recipe,
            target=recipe,
            serializer_class=FavoritesSerializer,
            response_serializer_class=ResponseFavoritesSerializer,
            data=data_to_response
        )
