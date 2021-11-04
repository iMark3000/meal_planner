import json
import django
django.setup()

# this below import might cause issues
from ..models import *


#	This uploads JSON data into Django
#	It is nearly perfect. Do not touch it
#   /s


class RecipeJsonUploader:

    def __init__(self):
        pass

    def _create_recipe_object(self):
        # recipe = Recipe()
        recipe_name = self.recipe_data['meta_data']['recipe_name']
        self.recipe = Recipe(recipe_name=recipe_name)
        self.recipe.website_name = self.recipe_data['meta_data']['website_name']
        self.recipe.website = self.recipe_data['meta_data']['website_address']
        self.recipe.recipe_author = self.recipe_data['meta_data']['recipe_author']
        self.recipe.recipe_description = self.recipe_data['meta_data']['recipe_description']
        self.recipe.save()

    def _recipe_ingredient_iter(self):
        for ingredient_component in self.recipe_data['ingredients']:
            component_name = ingredient_component['ingredient_component_name']
            ingredient_set_obj = self._create_recipe_ingredient_set_object(component_name)
            ingredient_set_obj.save()
            for ingredient_list in ingredient_component['ingredient_component_list']:
                ingredient = self._create_recipe_ingredient_object(**ingredient_list)
                ingredient.ingredient_set = ingredient_set_obj
                ingredient.save()

    def _create_recipe_ingredient_set_object(self, name):
        return RecipeIngredientSet(recipe=self.recipe, recipe_component_name=name)

    def _create_recipe_ingredient_object(self, ingredient, amount, unit):

        # Do not this this works
        if amount == 'NONE':
            amount = 0.0
        else:
            amount = amount

        name = ingredient
        ingredient_object, created = Ingredient.objects.get_or_create(
            ingredient_name=name
        )
        unit = unit
        return RecipeIngredients(amount=amount, unit_of_measurement=unit,
                                 ingredient=ingredient_object)

    def _recipe_instruction_iter(self):
        for instruction_set in self.recipe_data['instructions']:
            set_name = instruction_set['instruction_set_name']
            set_order = instruction_set['instruction_set_order']
            instruct_set_obj = self._create_recipe_instruction_set_object(set_name, set_order)
            instruct_set_obj.save()
            for instructions in instruction_set['instructions']:
                step = self._create_recipe_instruction_object(**instructions)
                step.instruction_set = instruct_set_obj
                step.save()

    def _create_recipe_instruction_set_object(self, name, order):
        return RecipeInstructionSet(recipe=self.recipe, instruction_set_name=name,
                                    instruction_order=order)

    def _create_recipe_instruction_object(self, instruction_step, instruction_text):
        step = instruction_step
        text = instruction_text
        return RecipeInstruction(step=step, instruction_text=text)

    def _file_intake(self):
        input_file = str(input('Give me the file path, please :)\n'))

        file = open(input_file, 'r')
        self.recipe_data = json.load(file)

    def driver(self):
        self._file_intake()
        self._create_recipe_object()
        self._recipe_ingredient_iter()
        self._recipe_instruction_iter()