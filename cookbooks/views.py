from .models import (Recipe, Ingredient,
                     deserialize_user,
                     Tags, deserialize_tags,
                     deserialize_tag, CategoryForTag,
                     Images, Difficulty,
                     deserialize_ingredient)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User


@api_view(['GET', 'POST'])
def recipe_pagination(request, page, format=None):
    '''
    like the name suggests the code gives you the list of recieps in a paginated format
    you have to check fi the list is empty or not and all that
    it is a long story and process but it is fun
    :param request:
    :param page:
    :param format:
    :return:
    '''
    if request.method == 'GET':
        recipes = Recipe.objects.all()
        if page:
            page_number = page
            page_bottom = (page - 1) * 5  # lower part fo the pagination like zero
            page_top = page_number * 5  # higher end opf the pagination like five
            counter = 0
            recipe_list = []
            boolean = 'not yet sure'
            for recipe in recipes:
                if counter >= page_bottom:
                    recipe_list.append(recipe.deserialize_recipe_slim())
                counter += 1
                if counter == page_top:
                    break
            return Response({
                'status': 'SUCCESS',
                'recipes': recipe_list,
            })


@api_view(['GET', 'POST'])
def recipe_list_or_add(request, format=None):
    """
    :param request:
    :return:
    function lists the recipes in our database and allows me to create a new recipe
    you can get all recipes with their id and their titles
    it allows you to post a recipe and it returns the full details of the recipe just posted just for testing sake
    """

    if request.method == 'GET':
        recipes = Recipe.objects.all()
        recipes_list = [
            {
                'id': recipe.id,
                'title': recipe.title,
            }
            for recipe in recipes
        ]

        return Response({
            'status': 'SUCCESS',
            'recipes': recipes_list,
        })

    elif request.method == 'POST':
        """
        FIX THIS AUTHOR PROBLEM        
        """
        author_id = request.data.get('author_id', None)
        title = request.data.get('title', None)
        instructions = request.data.get('instructions', None)
        ingredients_id = request.data.get('ingredients_id', None)
        difficulty_id = request.data.get('difficulty_id', None)
        time_to_complete = request.data.get('time_to_complete', None)
        tags = request.data.get('tags', None)

        if author_id and title and instructions and ingredients_id and difficulty_id:
            difficulty = Difficulty.objects.get(id=difficulty_id)
            time_to_complete = int(time_to_complete)
            author = User.objects.get(id=author_id)
            instance = Recipe.objects.create(
                title=title, author=author, instructions=instructions, difficulty=difficulty,
                time_to_complete=time_to_complete,
            )

            instance.save()
            for i in ingredients_id:
                """  
                add a try and catch block here to catch the errors 
                """
                ingredient = Ingredient.objects.get(id=i)
                instance.ingredients.add(ingredient)

            for t in tags:
                t = int(t)
                tag = Tags.objects.get(id=t)
                instance.tags.add(tag)
            data = {
                'status': 'SUCCESS',
                'recipe': instance.deserialize_recipe()
            }
            return Response(data)
        else:
            data = {
                'status': 'FAILED',
                'message': 'ERROR! check to see if you added all required **kwargs to create a recipe '
            }
            return Response(data)


@api_view(['GET', 'POST', 'DELETE'])
def recipe_detail_update_or_delete(request, pk, format=None):
    """
    :param request:
    :return:
    delete, update or retrieve a recipe
    It gives you  full details given you have the recipe id
    allows you to update a recipe and change anything you want in it
    """
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return Response({
            'status': 'NOT FOUND',
        })

    if request.method == 'GET':
        return Response(recipe.deserialize_recipe())

    elif request.method == 'POST':
        """
        UPDATE METHOD
        come back and update the code to handle all parts of the recipe 
        ALLOW YOU TO UPDATE THE FOLLOWING FOR NOW 
        Title, Ingredient, Instructions
        """
        if request.data.get('title', False):
            title = request.data['title']
            recipe.title = title
            recipe.save()
        if request.data.get('instructions', False):
            instructions = request.data['instructions']
            recipe.instructions = instructions
            recipe.save()
        if request.data.get('ingredients_id', False):
            ingredients_id = request.data['ingredients_id']
            recipe.ingredients.clear()
            for i in ingredients_id:
                """
                 SMART CODE TO ADD AND REMOVE INGREDIENTS AT WILL 
                 short code done and working perfectly
                """
                ingredient = Ingredient.objects.get(id=i)
                recipe.ingredients.add(ingredient)
        data = {
            'status': 'SUCCESS',
            'message': 'all stuff was updated',
            'recipe': recipe.deserialize_recipe()
        }
        return Response(data)

    elif request.method == 'DELETE':
        recipe.delete()
        return Response({
            'status': 'SUCCESS',
            'message': 'DELETED',
        })


@api_view(['GET', 'POST'])
def ingredient_list_or_add(request, format=None):
    '''
    allows a user to get the list of ingredients in the database
    it also allows a user to do simple things like create an ingredient


    what is to say they have not altered footage for the code


    
    :param request:
    :param format:
    :return:
    '''
    if request.method == 'GET':
        ingredients = Ingredient.objects.all()
        ingredient_list = [
            deserialize_ingredient(ingredient)
            for ingredient in ingredients
        ]
        return Response({
            'status': 'SUCCESS',
            'ingredients': ingredient_list,
        })

    elif request.method == 'POST':
        '''
        this part of the fubnction creates an ingredient 
        it is a simple functiojn and is easy to use 
        parameters required are 
        title description 
        vegetarian is optional 
        
        '''

        # set something like number given or so
        # do have a blast coding

        title = request.data.get('title', None)
        description = request.data.get('description', None)
        vegetarian = request.data.get('vegetarian', None)

        if vegetarian is not None and title and description:
            ingredient = Ingredient.objects.create(
                vegetarian=vegetarian,
                description=description,
                title=title,
            )
            ingredient.save()
        elif vegetarian is None and title and description:
            ingredient = Ingredient.objects.create(
                description=description,
                title=title,
            )
            ingredient.save()
        return Response({
            'status': 'SUCCESS',
            'ingredient': deserialize_ingredient(ingredient)
        })


@api_view(['GET', 'POST', 'DELETE'])
def ingredient_detail_update_or_delete(request, pk, format=None):
    """
    create a post that allows user to search for ingredients based on the id of the ingredient
    allows user to update an ingredient
    allows user to delete an ingredient

    :param request:
    :param pk:
    :param format:
    :return:

    """
    try:
        ingredient = Ingredient.objects.get(pk=pk)
    except Ingredient.DoesNotExist:
        return Response({
            'status': 'NOT FOUND'
        })

    if request.method == 'GET':
        data = deserialize_ingredient(ingredient)
        return Response(data)

    elif request.method == 'POST':
        """
        UPDATE METHOD
        
        ALLOWS YOU TO UPDATE THE FOLLOWING FOR NOW 
        
        Title, Ingredient, Instructions
        """
        if request.data.get('title', False):
            title = request.data['title']
            ingredient.title = title
            ingredient.save()
        if request.data.get('description', False):
            description = request.data['description']
            ingredient.description = description
            ingredient.save()
        if request.data.get('vegetarian', False):
            vegetarian = request.data['vegetarian']
            ingredient.vegetarian = vegetarian
            ingredient.save()
        data = {
            'status': 'SUCCESS',
            'message': 'UPDATED',
            'ingredient': deserialize_ingredient(ingredient)
        }
        return Response(data)

    elif request.method == 'DELETE':
        ingredient.delete()
        return Response({
            'status': 'SUCCESS',
            'message': 'DELETED',
        })


@api_view(['GET', 'POST'])
def recipe_list_by_tags(request, format=None):
    '''
    :param tag_name recipe_no tag_id
    :param request:
    :param format:
    :return: Usually the full list of recipes in the database
             it also gives us some more things like recipes based oin some tags
             another ting is recipes for asn endless s roler

    the function is a function that allows you to tget the list of recipes based on the tag
    you supply the tag you want either by name or by id
    then we check for the tag and give the recipes tah tr have it
    it can also supply null
    so be able to check for that in the code

    this code works like this. You write the tag you want and the number of recipes you want for the tag.
    The code will return to you the number of tags or better yet the number of recipes
    Enjoy Good Code!!!
    '''

    if request.method == 'POST':
        tag_name = request.data.get('tag_name', None)
        recipe_no = request.data.get('recipe_no', None)
        tag_id = request.data.get('tag_id', None)

        if tag_name and recipe_no:
            tag = Tags.objects.get(title=tag_name)
            recipe_list = Recipe.objects.filter(tags=tag)
            i = 0
            recipes_returned = []
            for recipe in recipe_list:
                recipes_returned.append(recipe.deserialize_recipe_slim())
                i += 1
                if i == recipe_no:
                    break
            return Response({
                'status': 'SUCCESS',
                'recipes': recipes_returned,
            })

        elif tag_id and recipe_no:
            tag = Tags.objects.get(id=tag_id)
            recipe_list = Recipe.objects.filter(tags=tag)
            i = 0
            recipes_returned = []
            for recipe in recipe_list:
                recipes_returned.append(recipe.deserialize_recipe_slim())
                i += 1
                if i == recipe_no:
                    break
            return Response({
                'status': 'SUCCESS',
                'recipes': recipes_returned,
            })


@api_view(['POST'])
def recipe_pagination_list_by_tags(request, page, format=None):
    '''
    :param tag_name recipe_no tag_id
    :param request:
    :param format:
    :return: Usually the full list of recipes in the database
             it also gives us some more things like recipes based oin some tags
             another ting is recipes for asn endless s roler
    Enjoy Good Code!!!

    '''
    if request.method == 'POST':
        tag_name = request.data.get('tag_name', None)
        tag_id = request.data.get('tag_id', None)
        if tag_name:
            tag = Tags.objects.get(title=tag_name)
            recipes = Recipe.objects.filter(tags=tag)
            page_number = page
            page_bottom = (page - 1) * 10 # lower part of the pagination like zero
            page_top = page_number * 10  # higher end of the pagination like ten...
            counter = 0
            recipe_list = []
            for recipe in recipes:
                if counter >= page_bottom:
                    recipe_list.append(recipe.deserialize_recipe_slim())
                counter += 1
                if counter == page_top:
                    break
            return Response({
                'status': 'SUCCESS',
                'recipes': recipe_list,
            })
        elif tag_id:
            tag = Tags.objects.get(id=tag_id)
            recipes = Recipe.objects.filter(tags=tag)
            page_number = page
            page_bottom = (page - 1) * 10 # lower part of the pagination like zero
            page_top = page_number * 10  # higher end of the pagination like ten...
            counter = 0
            recipe_list = []
            for recipe in recipes:
                if counter >= page_bottom:
                    recipe_list.append(recipe.deserialize_recipe_slim())
                counter += 1
                if counter == page_top:
                    break
            return Response({
                'status': 'SUCCESS',
                'recipes': recipe_list,
            })


@api_view(['GET', 'POST'])
def tag_pagination_list_by_categories(request, page, format=None):
    '''
    :param request:
    :param format:
    :return: Usually the full list of recipes in the database
             it also gives us some more things like recipes based oin some tags
             another ting is recipes for asn endless s roler
    the function is a function that allows you to tget
    the list of recipes based on the category of  the recie asked for
    '''
    if request.method == 'POST':
        category_tag_name = request.data.get('category_tag_name', None)
        category_tag_id = request.data.get('category_tag_id', None)
        if category_tag_name:
            category_for_tag = CategoryForTag.objects.get(title=category_tag_name)
            tags = category_for_tag.tags.all()
            # image_url = category_for_tag.tags.first().deserialize_tag()['image_url']
            page_number = page
            page_bottom = (page - 1) * 10 # lower part of the pagination like zero
            page_top = page_number * 10  # higher end of the pagination like ten...
            counter = 0
            tag_list = []
            for tag in tags:
                if counter >= page_bottom:
                    tag_list.append(tag.deserialize_tag())
                counter += 1
                if counter == page_top:
                    break
            return Response({
                'status': 'SUCCESS',
                'tags': tag_list,
            })
        elif category_tag_id:
            category_for_tag = CategoryForTag.objects.get(pk=category_tag_id)
            tags = category_for_tag.tags.all()
            # image_url = category_for_tag.tags.first().deserialize_tag()['image_url']
            page_number = page
            page_bottom = (page - 1) * 10 # lower part of the pagination like zero
            page_top = page_number * 10  # higher end of the pagination like ten...
            counter = 0
            tag_list = []
            for tag in tags:
                if counter >= page_bottom:
                    tag_list.append(tag.deserialize_tag())
                counter += 1
                if counter == page_top:
                    break
            return Response({
                'status': 'SUCCESS',
                'tags': tag_list,
            })
        else:
            return Response({
                'status': 'FAILED',
            })


@api_view(['GET', 'POST'])
def tag_pagination(request, page,  format=None):
    """
    :param request:
    :return:
    function lists the tags in our database and allows me to create a new tag based on new parameters
    ... I will only allow people who are making recipes to create a new tag or a new category! .
    for now i will review all categories created before letting them go scott free. !!
    that is good code. LOL.
    you can get all tags with their id and their titles
    """
    if request.method == 'GET':
        tags = Tags.objects.all()
        if page:
            page_number = page
            page_bottom = (page - 1) * 10 # lower part of the pagination like zero
            page_top = page_number * 10  # higher end of the pagination like ten...
            counter = 0
            tag_list = []
            for tag in tags:
                if counter >= page_bottom:
                    tag_list.append(tag.deserialize_tag())
                counter += 1
                if counter == page_top:
                    break
            return Response({
                'status': 'SUCCESS',
                'tags': tag_list,
            })


@api_view(['GET', 'POST', 'DELETE'])
def tag_detail_update_or_delete(request, pk, format=None):
    """
    create a post that allows user to search for tags
    allows user to update a tag
    allows user to delete a tag

    :param request:
    :param pk:
    :param format:
    :return:

    """
    try:
        tag = Tags.objects.get(pk=pk)
    except Tags.DoesNotExist:
        return Response({
            'status': 'NOT FOUND'
        })

    if request.method == 'GET':
        data = deserialize_tag(tag)
        return Response(data)

    elif request.method == 'POST':
        """
        UPDATE METHOD
        
        ALLOWS YOU TO UPDATE THE FOLLOWING FOR NOW 

        Title, Ingredient, Instructions
        """
        if request.data.get('title', False):
            title = request.data['title']
            tag.title = title
            tag.save()
        if request.data.get('description', False):
            description = request.data['description']
            tag.description = description
            tag.save()
        data = {
            'status': 'SUCCESS',
            'message': 'UPDATED',
            'tag': tag.deserialize_tag(),
        }
        return Response(data)

    elif request.method == 'DELETE':
        tag.delete()
        return Response({
            'status': 'SUCCESS',
            'message': 'DELETED',
        })


@api_view(['GET'])
def category_pagination(request, page,  format=None):
    """
    :param request:
    :return:
    code paginates a category you don't need more note from this/.
    Enjoy your code.

    """
    if request.method == 'GET':
        categories = CategoryForTag.objects.all()
        if page:
            page_number = page
            page_bottom = (page - 1) * 10 # lower part of the pagination like zero
            page_top = page_number * 10  # higher end of the pagination like ten...
            counter = 0
            category_list = []
            for category in categories:
                if counter >= page_bottom:
                    category_list.append(category.deserialize_category_for_tags())
                counter += 1
                if counter == page_top:
                    break
            return Response({
                'status': 'SUCCESS',
                'tags': category_list,
            })


def helper_function(item):
    print('heyu')


@api_view([ 'POST'])
def search_recipes_view(request,   format=None):
    """
    :param request:
    :return: recipes, ingredients and tags with grading systems called search grades.
    this function will return for you the results of your search for a recipe
    we ill return some typs of recieps
    like for one a recipe
    the next one will be to return  list ofg ingredients tht atre relsated or tags
    """
    if request.method == 'POST':
        search_query = request.data.get('search_query', None)
        new_list = []
        exclude = ['how', 'to', 'if', 'and', 'is', 'for', 'of', 'i', 'a', 'is']
        words = search_query.split()
        for word in words:
            if word not in exclude:
                new_list.append(word)
        complete_list = []
        if new_list is not []:
            for item in new_list:
                recipes = Recipe.objects.filter(title__icontains=item)
                for recipe in recipes:
                    j = recipe.deserialize_recipe()
                    complete_list.append(j)
            return Response({
                'search_results': complete_list,
                'status': 'SUCCESS',
            })
        else:
            return Response({
                'search_results': 0,
            })
        # if page:
        #     page_number = page
        #     page_bottom = (page - 1) * 10 # lower part of the pagination like zero
        #     page_top = page_number * 10  # higher end of the pagination like ten...
        #     counter = 0
        #     tag_list = []
        #     for tag in tags:
        #         if counter >= page_bottom:
        #             tag_list.append(tag.deserialize_tag())
        #         counter += 1
        #         if counter == page_top:
        #             break
        #     return Response({
        #         'status': 'SUCCESS',
        #         'tags': tag_list,
        #     })


def test_function(search_query):
    complete_list = []
    print('hello ')
    new_list = []
    exclude = ['how', 'to', 'if', 'and', 'is', 'for', 'of', 'i', 'a', 'is']
    words = search_query.split()
    for word in words:
        if word not in exclude:
            new_list.append(word)
    if new_list != []:
        for item in new_list:
            recipes = Recipe.objects.filter(title__icontains=item)
            for recipe in recipes:
                j = recipe.deserialize_recipe()
                if complete_list != []:
                    print('f  don reach here')
                    j_id = j['id']
                    j_id = int(j_id)
                    for element in complete_list:
                        if element['id'] == j_id:
                            print('f no get here')
                            element_points = element.points
                            element_points += 1
                            element['points'] = element_points
                        else:
                            print('f get here')
                            j['points'] = 1
                            complete_list.append(j)
                else:
                    print('f first reach here')
                    j['points'] = 1
                    complete_list.append(j)

        return complete_list


def new(arg):
    f = []
    for a in arg:
        print(a)
        f.append(a)
    return f
"""  
Now my job is to create a function that will return the tags given. 
 Enjoy Good Code
 fix the category for cards like you didi the tag cat 


a. Get the details about an ingredient ....DONE
b. create an ingredient ......NO NEED? 

d.  Get a pre-defined number of ingredients and recipes  from our database...  DOJNE
e. try and do auto completion... 
f. get recipes with varying levels of nutrients ... LATER
g. Add the image field to both or all of the things you are using ........WORKING ON THIS RIGHT NOW


CREATE AN INGREDIENT UNIT TABLE NDER THE RECIPE 

ALL USER TO GET RECIPES BASED ON NUTRIENT CONTENT 
LET USERS KNOW NUTRIENTS AND ALL 
HAVE FUN 


I WILL MAKE NEW TAGS FROM HERE 
SO THIS WILL BE BEAUTIFUL 
FINALLY TEST YOUR DATABASE 
REMEMBER TO USE PHONE MEMORY TO STORE RECIEPS AS PER BOOKMARKS

dont forget to 
wash clothews 
take bath 
call favour 
send cv 
call sisters 
call yemi 
call bisola 
code 
cook 
call friends or whatever 
create a bar like canva above your app 
for adverts and other sht 


CREATE PICTURES GET REAL DATA ADD AND TEST 

MAKE A FUNCTION THAt WILL SIMPLY CALCULATE THE NUTRIENT CNTENT OF A RECIPE IN TOTAL 

okay so firsi have to create a way to post the picturs in such a way that it is made to be so simple and i,o
STEP 1: b
    Find out how to save imaes to specific files or folders 
STEP 2@
    rename the code in such a way that out code snipppet is neat 

"""
