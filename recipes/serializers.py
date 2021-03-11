from rest_framework import serializers
from .models import User, Recipe, Ingredient, Rating

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

    """
    def create(self, validated_data):
        pswd = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if pswd is not None:
            instance.set_password(pswd)
        instance.save()
        return instance"""



class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['ingredientName']



class RecipeSerializer(serializers.ModelSerializer):

    creator = UserSerializer()
    ingredient = IngredientSerializer(many=True)

    def get_creator(self, obj):
        return obj.creator.username

    class Meta:
        model = Recipe
        fields = ['id', 'recipeName', 'recipeText', 'creator', 'ingredient']
