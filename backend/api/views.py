from api.serializers import (CustomUserSerializer, FavoritesSerializer,
                             FollowSerializer, IngredientSerializer,
                             RecipeCreateSerializer, RecipeSerializer,
                             ResponseFavoritesSerializer, TagSerializer)
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
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        user_author = Follow.objects.filter(user=user, author=author)
        if not user_author.exists():
            return Response({
                'errors': 'string',
            }, status=status.HTTP_400_BAD_REQUEST
            )
        elif request.method == 'POST':
            serializer = FollowSerializer(data={
                'user': user.id,
                'author': author.id
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = CustomUserSerializer(user)
            import pdb;pdb.set_trace()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            user_author.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


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
        if not user_recipe.exists():
            return Response({
                'errors': 'string',
            }, status=status.HTTP_400_BAD_REQUEST
            )
        elif request.method == 'POST':
            serializer = FavoritesSerializer(data={
                'user': user.id,
                'recipe': recipe.id
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = ResponseFavoritesSerializer(recipe)
            #import pdb;pdb.set_trace()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            user_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

