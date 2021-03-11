from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True, default=True)


class Ingredient(models.Model):
    ingredientName = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.ingredientName


class Recipe(models.Model):
    recipeName = models.CharField(max_length=255, null=False, blank=False)
    recipeText = models.TextField(max_length=2000, null=False, blank=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ManyToManyField(Ingredient)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipeName', 'creator'], name='unique_recipe')
        ]

    def __str__(self):
        return self.recipeName


class Rating(models.Model):
    score = models.IntegerField(blank=False, null=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'user'], name='unique_score'),
            models.CheckConstraint(
                check=models.Q(score__gte=1) & models.Q(score__lte=10),
                name="score_range",
            )
        ]

    def __str__(self):
        return 'Score for ' + self.recipe.recipeName + ' by ' + self.user.username

