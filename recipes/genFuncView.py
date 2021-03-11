from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, RecipeSerializer, IngredientSerializer
from .models import User, Recipe, Rating, Ingredient
from .helperFunctions import aggregate, sortAndReturnN, addFieldAndCollectData


class allRecipesView(APIView):
    def get(self, request):
        data = map(lambda x : RecipeSerializer(x).data, Recipe.objects.all())
        return Response(data)

class recipeView(APIView):
    def get(self, request, recipe_id):
        data = RecipeSerializer(Recipe.objects.get(id=recipe_id)).data
        return Response(data)


class topRecipesView(APIView):
    def get(self, request, n):
        calculatedScores = aggregate(Rating, 'recipe', Avg, 'score')
        sortedRecipes = sortAndReturnN(calculatedScores, lambda x : -x['aggregation'], n)
        data = map(lambda x : addFieldAndCollectData(RecipeSerializer, Recipe, x['recipe'], 'avg_score', x['aggregation']), sortedRecipes)

        return Response(data)
    

class topIngredientsView(APIView):
    def get(self, request, n):
        countedIngredients = aggregate(Recipe, 'ingredient', Count, 'ingredient')
        countedIngredients = sortAndReturnN(countedIngredients, lambda x : -x['aggregation'], n)
        data =  map(lambda x : addFieldAndCollectData(IngredientSerializer, Ingredient, x['ingredient'], 'count', x['aggregation']), countedIngredients)

        return Response(data)