from django.contrib import admin
from django.urls import path, include
from .userRecipesView import userRecipesView, makeRecipeView, editRecipeView, scoreRecipeView

urlpatterns = [
    path('myrecipes/', userRecipesView.as_view()),
    path('scorerecipe/<int:recipe_id>', scoreRecipeView.as_view()),
    path('makerecipe/', makeRecipeView.as_view()),
    path('editrecipe/<int:recipe_id>', editRecipeView.as_view()),
]