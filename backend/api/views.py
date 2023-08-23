import tempfile

from api.serializers import (CartSerializer, CustomUserSerializer,
                             FavoriteSerializer, FollowSerializer,
                             IngredientSerializer, RecipeCreateSerializer,
                             RecipeSerializer, ResponseFavoriteSerializer,
                             ResponseSubscribeSerializer, TagSerializer)
from core.action_method import save_delete_action
from core.creation_pdf import make_shopping_cart
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.http import urlquote
from djoser.views import UserViewSet
from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag
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
        queryset = User.objects.filter(following__author=request.user)
        serializer = ResponseSubscribeSerializer(many=True, data=queryset)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        with tempfile.NamedTemporaryFile(delete=False) as temp_pdf_file:
            temp_filename = temp_pdf_file.name

        make_shopping_cart(request.user, temp_filename)

        with open(temp_filename, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        response = HttpResponse(pdf_content, content_type='application/pdf')
        filename = urlquote(f"shopping_list_{request.user}.pdf")
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
