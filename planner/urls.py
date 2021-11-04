from django.urls import path

from . import views

app_name = 'planner'
urlpatterns = [
    path('<int:recipe_id>/recipe', views.recipe, name='recipe'),
    path('search', views.search, name='search'),
]
