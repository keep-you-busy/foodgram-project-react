from core.extra_fields import Base64ImageField, Hex2NameColor
from django.db.models import F
from djoser.serializers import UserSerializer
from recipes.models import Favorites, Ingredient, IngredientRecipe, Recipe, Tag
from rest_framework import serializers
from users.models import Follow, User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
    read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')
        read_only_fields = ("__all__",)

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')
        read_only_fields = ("__all__",)

class RecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientSerializer(many=True)


    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorites.objects.filter(user=user, author=obj).exists()

    #def get_ingredients(self, obj):
    # take care of getting list of the ingredients
