from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Recipe, PlannedMeal
from .filters import SearchFilter
from .forms import PlannedRecipeEventForm


@login_required
def recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)

    if request.method == 'POST':
        form = PlannedRecipeEventForm(request.POST)

        if form.is_valid():
            if request.user.is_authenticated:
                planned_meal = PlannedMeal()
                planned_meal.recipe = recipe
                planned_meal.user = request.user
                planned_meal.date = form.cleaned_data['date']
                planned_meal.save()
            return HttpResponseRedirect(reverse('dashboard'))

    else:
        form = PlannedRecipeEventForm()

    # Gathering Ingredients
    ingredient_headers = True
    ingredient_info = {}
    recipe_ingredient_set = recipe.recipeingredientset_set.all()
    print(len(recipe_ingredient_set))

    for component in recipe_ingredient_set:
        component_name = component.recipe_component_name.capitalize()
        component_ingredients = component.recipeingredients_set.all()
        ingredient_list = []
        for ingredients in component_ingredients:
            ingredient_list.append(ingredients.get_recipe_ingredient_info())

        ingredient_info[component_name] = ingredient_list

    if len(recipe_ingredient_set) == 1:
        print('here')
        ingredient_headers = False

    # Gathering Instructions
    instruction_headers = True
    instruction_info = {}
    recipe_instruction_set = recipe.recipeinstructionset_set.all().order_by('instruction_order')

    for instruction_set in recipe_instruction_set:
        instruction_set_name = instruction_set.instruction_set_name.capitalize()
        steps = instruction_set.recipeinstruction_set.all().order_by('step')
        instruction_list = []
        for instruction in steps:
            instruction_list.append(instruction.instruction_text.capitalize())

        instruction_info[instruction_set_name] = instruction_list

    if len(recipe_instruction_set) == 1:
        instruction_headers = False

    context = {
        'recipe': recipe,
        'form': form,
        'ingredient_headers': ingredient_headers,
        'ingredient_info': ingredient_info,
        'instruction_headers': instruction_headers,
        'instruction_info': instruction_info
    }

    return render(request, 'planner/recipe.html', context=context)


def search(request):
    # Read this: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
    recipes = Recipe.objects.all()

    # form = PlannedRecipeEventForm()

    search_filter = SearchFilter(request.GET, queryset=recipes)
    recipes = search_filter.qs

    context = {
        'recipe': recipes,
        'filter': search_filter,
    }

    return render(request, 'planner/search.html', context)
