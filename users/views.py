import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# this import works when running manage.py
# will this always work when running django?
from planner.models import PlannedMeal


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def dashboard(request):
    if request.user.is_authenticated:
        dashboard_user = request.user

    today = datetime.date.today()
    meals_plans = dashboard_user.plannedmeal_set.filter(date__gte=today).order_by('date')[:5]

    return render(request, 'users/dashboard.html', {'meals': meals_plans})


@login_required
def grocery_list(request):
    if request.user.is_authenticated:
        grocery_user = request.user

    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=6)
    meals_for_week = grocery_user.plannedmeal_set.filter(date__range=[start_date,
                                                                      end_date])

    ingredient_obj = []

    for meal in meals_for_week:
        recipe = meal.recipe
        ingredient_set = recipe.recipeingredientset_set.all()
        for iSet in ingredient_set:
            ingredient = iSet.recipeingredients_set.all()
            for i in ingredient:
                ingredient_obj.append(i)

    # ingredient_obj.sort(key=lambda x: x.ingredient, reverse=True)

    context = {
        'ingredients': ingredient_obj,
        'date_end': end_date,
    }

    return render(request, 'users/grocery_list.html', context)
