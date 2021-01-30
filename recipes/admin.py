from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Recipe)
admin.site.register(models.Instructions)
admin.site.register(models.Nutrients)
admin.site.register(models.Ingredient)



