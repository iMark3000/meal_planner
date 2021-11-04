from django.contrib import admin

from .models import *


# Register your models here.
class PlannerAdmin(admin.ModelAdmin):
    list_display = ("recipe_name",)


admin.site.register(Recipe, PlannerAdmin)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredients)
admin.site.register(RecipeKeywords)
admin.site.register(RecipeInstruction)