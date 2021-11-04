import django_filters
from django_filters import CharFilter
from .models import *


class SearchFilter(django_filters.FilterSet):
    # recipe = CharFilter(field_name='recipe_name', lookup_expr='__contains')
    class Meta:
        model = Recipe
        fields = {
            'recipe_name': ['icontains'],
            'recipe_website_name': ['icontains'],
            'recipe_description': ['icontains'],
            'recipe_author': ['icontains']
        }