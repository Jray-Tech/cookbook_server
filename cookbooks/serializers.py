from rest_framework import serializers
from .models import Recipe, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id' , 'title', 'description', 'carbohydrate', 'protein', 'unit']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'author', 'ingredients', 'instructions', 'date_posted']


"""
lets serialize sme shit man and code good code
"""