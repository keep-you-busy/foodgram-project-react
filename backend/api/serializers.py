from collections import OrderedDict

from core.extra_fields import Base64ImageField, Hex2NameColor
from django.db.models import F
from djoser.serializers import UserSerializer
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)
from rest_framework import serializers
from rest_framework.relations import Hyperlink, PKOnlyObject
from users.models import Follow, User


class CustomUserSerializer(UserSerializer):
    """Сериализатор для модели Пользователей.

    Дополнительно обрабатывает булевое значение подписки пользователя
    на автора.
    """

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
    """Сериализатор для модели Тегов."""

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('__all__',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('__all__',)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ингредиентов, связанной по первичному ключу."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Рецептов.

    Дополнительно обрабатывает булевое значение подписки пользователя
    на автора.
    """

    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()


    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Cart.objects.filter(user=user, recipe=obj).exists()

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipes__ingredientrecipe__amount')
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания или изменения в модели Рецепта."""

    ingredients = IngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientRecipe.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.name = validated_data.get(
            'name', instance.name
        )
        instance.text = validated_data.get(
            'text', instance.text
        )
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        instance.ingredients.clear()
        instance.tags.set(tags)
        for ingredient in ingredients:
            IngredientRecipe.objects.update_or_create(
                recipe=instance,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        context = self.context.copy()
        context['request'] = self.context.get('request')
        recipe_serializer = RecipeSerializer(instance, context=context)
        return recipe_serializer.data


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Подписок."""

    class Meta:
        model = Follow
        fields = (
            'user',
            'author'
        )

    def validate(self, attrs):
        user = attrs.get('user')
        author = attrs.get('author')
        if user == author:
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписаться на себя самого!'}
            )
        return attrs

class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Списка покупок."""

    class Meta:
        model = Cart
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Избранное."""

    class Meta:
        model = Favorite
        fields = '__all__'


class ResponseSubscribeSerializer(CustomUserSerializer):
    """Сериализатор для методов подписок.

    Ограничивает выдачу рецептов по запросу,
    выдаёт количество объектов рецепта в базе данных по подписке.
    """

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'

        )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        recipes_limit = self.context.get('recipes_limit')
        if recipes_limit is not None:
            recipes_limit = int(recipes_limit)
            data['recipes'] = data['recipes'][:recipes_limit]
            data['recipes_count'] = min(recipes_limit, data['recipes_count'])

        return data

    def get_recipes(self, obj):
        return obj.recipes.values(
            'id',
            'name',
            'image',
            'cooking_time'
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class ResponseFavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для методов избранного."""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
