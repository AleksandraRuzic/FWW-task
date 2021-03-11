from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer, RecipeSerializer
from .models import User, Recipe, Ingredient, Rating
from .helperFunctions import checkIfLogedIn, isRecipeCreator, aggregate


class userRecipesView(APIView):
    def get(self, request):
        user = UserSerializer(checkIfLogedIn(request)).data
        userRecipes = Recipe.objects.filter(creator=user['id'])
        data = map(lambda x : RecipeSerializer(x).data, userRecipes)
        return Response(data)



class makeRecipeView(APIView):
    def post(self, request):
        user = checkIfLogedIn(request)
        data = request.data
        data['creator'] = user
        r = Recipe(recipeName=data['recipeName'], recipeText=data['recipeText'], creator=data['creator'])
        r.save()
        r.ingredient.set(Ingredient.objects.filter(pk__in=data['ingredient']))
        return Response(RecipeSerializer(r).data)




class editRecipeView(APIView):
    def get(self, request, recipe_id):
        userObj = checkIfLogedIn(request)
        recipeObj = Recipe.objects.filter(id=recipe_id)
        if not isRecipeCreator(userObj, recipeObj):
            raise AuthenticationFailed('Not your recipe mate!')
        return Response({"msg":"Edit your recipe!"})


    def post(self, request, recipe_id):
        userObj = checkIfLogedIn(request)
        recipeObj = Recipe.objects.filter(id=recipe_id)
        if not isRecipeCreator(userObj, recipeObj):
            raise AuthenticationFailed('Not your recipe mate!')

        recipeObj.update(recipeName=request.data['recipeName'], recipeText=request.data['recipeText'])
        recipeObj.first().ingredient.set(Ingredient.objects.filter(pk__in=request.data['ingredient']))
        return Response(RecipeSerializer(recipeObj.first()).data)


    

class scoreRecipeView(APIView):
    def get(self, request, recipe_id):
        userObj = checkIfLogedIn(request)
        recipeObj = Recipe.objects.filter(id=recipe_id)
        if isRecipeCreator(userObj, recipeObj):
            raise AuthenticationFailed("Can't score your own recipe mate!")
        return Response({"msg":"Enter your score!"})


    def post(self, request, recipe_id):
        userObj = checkIfLogedIn(request)
        recipeObj = Recipe.objects.filter(id=recipe_id)
        if isRecipeCreator(userObj, recipeObj):
            raise AuthenticationFailed("Can't score your own recipe mate!")

        rate = Rating(recipe=recipeObj.first(), user=userObj, score=request.data['score'])
        rate.save()
        return Response({"msg":"Bravooo"})