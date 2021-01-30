from django.contrib import admin
from .models import Recipe, Ingredient, Tags, CategoryForTag, Difficulty, Images
# REGISTERED MODELS

admin.site.register(Images)
admin.site.register(Recipe)
admin.site.register(Difficulty)
admin.site.register(Ingredient)
admin.site.register(Tags)
admin.site.register(CategoryForTag)