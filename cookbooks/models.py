from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import ast
import json


def deserialize_user(user):
    """
    deserializes user instance to json
    :param user:
    :return:
    """
    return {
        'id': user.id,
        'e-mail': user.email,
        'username': user.username,
    }


def deserialize_user_id(user):
    return {
        'id': user.id,
    }


def deserialize_ingredient(ing):
    return {
        'id': ing.id,
        'title': ing.title,
        'description': ing.description,
        'carbohydrate': ing.carbohydrate,
        'protein': ing.protein,
        'vegetarian': ing.vegetarian
        }


def deserialize_ing_id(ing):
    return {
        'id': ing.id,
    }


def deserialize_difficulty(difficulty):
    return difficulty.title


def deserialize_ingredients(ingredients):
    """
    deserializes ingredient instance to json
    :param ingredient:
    :return:
    """
    ing_list = [
        deserialize_ing_id(ing)
        for ing in ingredients
    ]
    return ing_list


def deserialize_tag(tag):
    return {
        'id': str(tag.id),
        'title': tag.title,
        'description': tag.description,
    }


def deserialize_tags(tags):
    tag_list = [
        deserialize_tag(tag)
        for tag in tags
    ]
    return tag_list


# this is where i write my custom code
class ListField(models.TextField):
    description = 'sub class for the django models it stores a list f values'

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []
        if isinstance(value, list):
            return  value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value


class Tags(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.title

    def get_image_url(self):
        value = self.recipe_set.first().recipe_image.url
        return value
    # to this code i want to add something like recipe attached to tag is ...
    # the image url of te first recipe in this tg is so so and so
    # that is what ui want to do
    # let us see how we can do some reverse look up
    # and add the functionality to our code for good sakes or cus i am awesome

    def deserialize_tag(self):
        return {
            'title': self.title,
            'description': self.description,
            'id': str(self.id),
            'image_url': self.recipe_set.first().recipe_image.url,
        }


class CategoryForTag(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.title

    def deserialize_category_for_tags(self):
        return {
            'title': self.title,
            'id': str(self.id),
            'description': self.description,
            'image_url': self.tags.first().recipe_set.first().recipe_image.url,
        }


class Ingredient(models.Model):
    title = models.CharField( max_length=50)
    description = models.CharField(max_length=500)
    carbohydrate = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    protein = models.DecimalField(blank=True, null=True,  max_digits=5, decimal_places=2)
    vegetarian = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Difficulty(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


def upload_path(instance, filename):
    return '/'.join(['recipes', str(instance.title), filename])


class Recipe (models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    instructions = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    difficulty = models.ForeignKey(Difficulty, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tags)
    time_to_complete = models.IntegerField()
    recipe_image = models.ImageField(default='/recipes/default/default.jpg', upload_to=upload_path)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def deserialize_recipe(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'author': deserialize_user(self.author),
            'ingredients': deserialize_ingredients(self.ingredients.all()),
            'instructions': self.instructions,
            'date_posted': self.date_posted,
            'difficulty': deserialize_difficulty(self.difficulty),
            'tags': deserialize_tags(self.tags.all()),
            'time_to_complete': self.time_to_complete,
            'image_url': self.recipe_image.url,
        }

    def deserialize_recipe_slim(self):
        return {
            'id': str(self.id),
            'key': str(self.id),
            'title': self.title,
            'author': deserialize_user(self.author),
            'difficulty': deserialize_difficulty(self.difficulty),
            'time_to_complete': self.time_to_complete,
            'image_url': self.recipe_image.url,
        }


class IngredientUnit(models.Model):
    unit = models.CharField(max_length=3)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class RecipeNutrient(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    carbohydrate = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    protein = models.DecimalField(blank=True, null=True,  max_digits=5, decimal_places=2)


class Images(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

