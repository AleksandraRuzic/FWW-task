from django.contrib import admin
from django.urls import path, include
from .genFuncView import allRecipesView, recipeView, topRecipesView, topIngredientsView

urlpatterns = [
    path('allrecipes/', allRecipesView.as_view()),
    path('toprecipes/<int:n>', topRecipesView.as_view()),
    path('topingredient/<int:n>', topIngredientsView.as_view()),
    path('recipe/<int:recipe_id>', recipeView.as_view()),
]