from django.db import models
from django.contrib.auth.models import User

'''
So here arfe the things i want for my shit 
a. Title
b. Description
c. Instructions
d. ingredients
e. Ratings
f. Date Posted
g. Some other stuff 
lets get started lol 
'''


class Ingredient(models.Model):
    title = models.CharField( max_length=50)
    description = models.CharField(max_length=500)
    carbohydrate = models.IntegerField(blank=True, null=True)
    protein = models.IntegerField(blank=True, null=True)
    unit = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    instructions = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

