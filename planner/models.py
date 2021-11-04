from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    recipe_website = models.CharField(max_length=200, default='Unknown')
    recipe_website_name = models.CharField(max_length=200, default='Unknown')
    recipe_author = models.CharField(max_length=200, default='Unkown')
    # recipe_keywords = models.ForeignKey("RecipeKeywords", on_delete=models.CASCADE)
    recipe_description = models.TextField(default='No Description Available')

    def __str__(self):
        return self.recipe_name


class RecipeIngredientSet(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    recipe_component_name = models.CharField(max_length=200, default='Main')

    def __str__(self):
        return f'Ingredients for {self.recipe} - {self.recipe_component_name} component'


class RecipeIngredients(models.Model):
    ingredient_set = models.ForeignKey(RecipeIngredientSet, on_delete=models.CASCADE)
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    unit_of_measurement = models.CharField(max_length=200)

    def amount_string_conversion(self):
        if self.amount == 0:
            return ''
        elif self.amount < 1.0:
            return self._fraction_conversion(self.amount)
        elif self.amount >= 1.0:
            whole_number = str(int(self.amount))
            if self.amount % 1 != 0:
                fraction = self._fraction_conversion(self.amount % 1)
                return f'{whole_number} {fraction}'
            else:
                return whole_number

    def _fraction_conversion(self, amount):
        if amount == 0.125:
            return f'1/8'
        elif amount == 0.25:
            return '1/4'
        elif amount == 0.33:
            return '1/3'
        elif amount == 0.5:
            return '1/2'
        elif amount == 0.75:
            return '3/4'

    def unit_of_measurement_converstion(self):
        if self.unit_of_measurement.lower() == 'none':
            return ''
        else:
            return self.unit_of_measurement

    def get_recipe_ingredient_info(self):
        ingredient_name = self.ingredient.ingredient_name
        amount = self.amount_string_conversion()
        unit_of_measurement = self.unit_of_measurement_converstion()
        return f'{amount} {unit_of_measurement} {ingredient_name}'

    def __str__(self):
        return f'{self.amount} {self.unit_of_measurement} {self.ingredient}'


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.ingredient_name


class RecipeInstructionSet(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, default='NONE')
    instruction_set_name = models.CharField(max_length=200)
    instruction_order = models.IntegerField()

    def __str__(self):
        return f'Instruction for {self.instruction_set_name} for Recipe: {self.recipe}'


class RecipeInstruction(models.Model):
    instruction_set = models.ForeignKey(RecipeInstructionSet, on_delete=models.CASCADE)
    step = models.IntegerField()
    instruction_text = models.TextField()

    def __str__(self):
        step = self.step + 1
        return f'Step {step} - {self.instruction_text}'


# Make keywords unique???
class RecipeKeywords(models.Model):
    keyword = models.CharField(max_length=200)
    recipe_keywords = models.ManyToManyField("Recipe")


class PlannedMeal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date = models.DateField()


# def _planned_meal_date_string(self):
#	return self.date.strftime('%A, %B %d, %Y')

# def __str__(self):
#	string_date = self._planned_meal_date_string()
#	return f'{self.recipe} planned for {string_date}'
from django.db import models

# Create your models here.
