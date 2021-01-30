from django.urls import path, include
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path('recipes/', recipe_list_or_add),
    path('recipes/<int:pk>/', recipe_detail_update_or_delete),
    path('recipes/page/<int:page>/', recipe_pagination),
    path('tags/pages/<int:page>/', tag_pagination),
    path('tags/<int:pk>/', tag_detail_update_or_delete),
    path('recipes/tag/', recipe_list_by_tags),
    path('recipes/tag/page/<int:page>/', recipe_pagination_list_by_tags),
    path('ingredients/', ingredient_list_or_add),
    path('ingredients/<int:pk>/', ingredient_detail_update_or_delete),
    path('categories/tags/page/<int:page>/', tag_pagination_list_by_categories),
    path('categories/page/<int:page>/', category_pagination),
    # make this paginated
    path('search/recipes/', search_recipes_view),
    # make it paginated for your code ... You wll use postgress sql so don't worry

]
urlpatterns = format_suffix_patterns(urlpatterns)