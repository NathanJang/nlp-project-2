import json
from copy import deepcopy
import random
import re


class Transformer:

  def __init__(self):
    self.words_file_name = 'word_list.json'

    with open(self.words_file_name, 'r') as words_file:
      self.words_json = json.load(words_file)

    self.transformation_mapping = {
      1: self.to_non_vegetarian,
      2: self.to_vegetarian,
      3: self.to_non_healthy,
      4: self.to_healthy,
      5: self.to_asian_cuisine,
    }

  def __getitem__(self, category):
    return self.words_json.get(category, [])

  def to_vegetarian(self, original_recipe):
    '''Returns a new vegetarian recipe using to the recipe dictionary representation in recipeFetcher.py'''
    new_recipe = deepcopy(original_recipe)
    replacements = {} # Mapping meaty ingredient -> new vegetarian ingredient
    for i, ingredient in enumerate(new_recipe['ingredients']):
      tokens = ingredient.split()
      if any(token in self['containsMeat'] for token in tokens):
        # We've found a meaty ingredient! Replace it with a random veg protein
        old_ingredient_t = next(iter(token for token in tokens if token in self['containsMeat']))
        new_ingredient_t = replacements.get(old_ingredient_t, random.choice(self['vegetarianProteins'])) # use existing or choose new replacement
        replacements[old_ingredient_t] = new_ingredient_t
        new_recipe['ingredients'][i] = ingredient.replace(old_ingredient_t, new_ingredient_t) # Put the replacement into new ingredient list
    # Loop through directions and stupidly replace tokens that are the old ingredient
    for i, direction in enumerate(new_recipe['directions']):
      direction = direction.replace("Watch Now", "") #remove "Watch Now" substring
      tokens = direction.split()
      for j, token in enumerate(tokens):
        if token in replacements:
          tokens[j] = replacements[token]
      new_direction = ' '.join(tokens)
      new_recipe['directions'][i] = new_direction
    return new_recipe

  def to_non_vegetarian(self, original_recipe):
    '''Returns a new non-vegetarian recipe using to the recipe dictionary representation in recipeFetcher.py'''
    new_recipe = deepcopy(original_recipe)
    replacements = {} # Mapping meaty ingredient -> new vegetarian ingredient
    for i, ingredient in enumerate(new_recipe['ingredients']):
      tokens = ingredient.split()
      if any(token in self['vegetarianProteins'] for token in tokens):
        # We've found a meaty ingredient! Replace it with a random veg protein
        old_ingredient_t = next(iter(token for token in tokens if token in self['vegetarianProteins']))
        new_ingredient_t = replacements.get(old_ingredient_t, random.choice(self['containsMeat'])) # use existing or choose new replacement
        replacements[old_ingredient_t] = new_ingredient_t
        new_recipe['ingredients'][i] = ingredient.replace(old_ingredient_t, new_ingredient_t) # Put the replacement into new ingredient list
    # Loop through directions and stupidly replace tokens that are the old ingredient
    for i, direction in enumerate(new_recipe['directions']):
      direction = direction.replace("Watch Now", "") #remove "Watch Now" substring
      tokens = direction.split()
      for j, token in enumerate(tokens):
        if token in replacements:
          tokens[j] = replacements[token]
      new_direction = ' '.join(tokens)
      new_recipe['directions'][i] = new_direction
    return new_recipe

  def to_healthy(self, original_recipe):
    '''Returns a new vegetarian recipe using to the recipe dictionary representation in recipeFetcher.py'''
    new_recipe = deepcopy(original_recipe)
    replacements = {}  # Mapping unhealthy ingredient -> new healthy ingredient
    for i, ingredient in enumerate(new_recipe['ingredients']):
      tokens = ingredient.split()
      for unhealthy_ingredient in self['healthyReplacements'].keys():
        if unhealthy_ingredient in ingredient:
          # We've found an unhealthy ingredient! Replace it
          old_ingredient_t = unhealthy_ingredient
          new_ingredient_t = replacements.get(old_ingredient_t, self['healthyReplacements'][old_ingredient_t])  # use existing or choose new replacement
          replacements[old_ingredient_t] = new_ingredient_t
          new_recipe['ingredients'][i] = ingredient.replace(old_ingredient_t, new_ingredient_t)  # Put the replacement into new ingredient list
          break
      if any(token == 'sugar' or token == 'salt' for token in tokens):
        # Halves sugar and salt
        quantity_pattern = re.compile('(?<!/)[\\d\\.]+(?!/)') # looks for a number that isn't a fraction
        match = quantity_pattern.search(ingredient)
        if not match: continue
        new_quantity = float(match[0]) / 2
        the_range = match.span()
        new_ingredient = ingredient[:the_range[0]] + str(new_quantity) + ingredient[the_range[1]:]
        new_recipe['ingredients'][i] = new_ingredient
    # Loop through directions and stupidly replace tokens that are the old ingredient
    for i, direction in enumerate(new_recipe['directions']):
      direction = direction.replace("Watch Now", "")  # remove "Watch Now" substring
      for original, replacement in replacements.items():
        if original in direction:
          new_direction = direction.replace(original, replacement)
          new_recipe['directions'][i] = new_direction
    return new_recipe

  def to_unhealthy(self, original_recipe):
    '''Returns a new vegetarian recipe using to the recipe dictionary representation in recipeFetcher.py'''
    new_recipe = deepcopy(original_recipe)
    replacements = {}  # Mapping unhealthy ingredient -> new healthy ingredient
    for i, ingredient in enumerate(new_recipe['ingredients']):
      tokens = ingredient.split()
      for unhealthy_ingredient in self['unhealthyReplacements'].keys():
        if unhealthy_ingredient in ingredient:
          # We've found a healthy ingredient! Replace it
          old_ingredient_t = unhealthy_ingredient
          new_ingredient_t = replacements.get(old_ingredient_t, self['unhealthyReplacements'][old_ingredient_t])  # use existing or choose new replacement
          replacements[old_ingredient_t] = new_ingredient_t
          new_recipe['ingredients'][i] = ingredient.replace(old_ingredient_t, new_ingredient_t)  # Put the replacement into new ingredient list
          break
      if any(token == 'sugar' or token == 'oil' or token == 'butter' for token in tokens):
        # Doubles sugar and oil
        quantity_pattern = re.compile('(?<!/)[\\d\\.]+(?!/)') # looks for a number that isn't a fraction
        match = quantity_pattern.search(ingredient)
        if not match: continue
        new_quantity = float(match[0]) * 2
        the_range = match.span()
        new_ingredient = ingredient[:the_range[0]] + str(new_quantity) + ingredient[the_range[1]:]
        new_recipe['ingredients'][i] = new_ingredient
    # Loop through directions and stupidly replace tokens that are the old ingredient
    for i, direction in enumerate(new_recipe['directions']):
      direction = direction.replace("Watch Now", "")  # remove "Watch Now" substring
      for original, replacement in replacements.items():
        if original in direction:
          new_direction = direction.replace(original, replacement)
          new_recipe['directions'][i] = new_direction
    return new_recipe

  # TODO
  def to_asian_cuisine(self):
    pass

  # TODO
  def to_non_healthy(self):
    pass


if __name__ == '__main__':
  testClass = Transformer()
  old_recipe =  {
    'ingredients': ['12 whole wheat lasagna noodles',
    '1 pound lean ground beef',
    '2 cloves garlic, chopped',
    '1/2 teaspoon garlic powder',
    '1 teaspoon dried oregano, or to taste',
    'salt and ground black pepper to taste',
    '1 (16 ounce) package cottage cheese',
    '2 eggs',
    '1/2 cup shredded Parmesan cheese',
    '1 1/2 (25 ounce) jars tomato-basil pasta sauce',
    '2 cups shredded mozzarella cheese'],
   'directions': ['Preheat oven to 350 degrees F (175 degrees C).\n                                    Watch Now',
    'Fill a large pot with lightly salted water and bring to a rolling boil over high heat. Once the water is boiling, add the lasagna noodles a few at a time, and return to a boil. Cook the pasta uncovered, stirring occasionally, until the pasta has cooked through, but is still firm to the bite, about 10 minutes. Remove the noodles to a plate.\n                                    Watch Now',
    'Place the ground beef into a skillet over medium heat, add the garlic, garlic powder, oregano, salt, and black pepper to the skillet. Cook the meat, chopping it into small chunks as it cooks, until no longer pink, about 10 minutes. Drain excess grease.\n                                    Watch Now',
    'In a bowl, mix the cottage cheese, eggs, and Parmesan cheese until thoroughly combined.\n                                    Watch Now',
    'Place 4 noodles side by side into the bottom of a 9x13-inch baking pan; top with a layer of the tomato-basil sauce, a layer of ground beef mixture, and a layer of the cottage cheese mixture. Repeat layers twice more, ending with a layer of sauce; sprinkle top with the mozzarella cheese. Cover the dish with aluminum foil.\n                                    Watch Now',
    'Bake in the preheated oven until the casserole is bubbling and the cheese has melted, about 30 minutes. Remove foil and bake until cheese has begun to brown, about 10 more minutes. Allow to stand at least 10 minutes before serving.\n                                    Watch Now'],
   'nutrition': [{'name': 'Total Fat',
     'amount': '19.3',
     'unit': 'g',
     'daily_value': '30 %'},
    {'name': 'Saturated Fat', 'amount': '9.0', 'unit': 'g', 'daily_value': None},
    {'name': 'Cholesterol',
     'amount': '115',
     'unit': 'mg',
     'daily_value': '38 %'},
    {'name': 'Sodium', 'amount': '999', 'unit': 'mg', 'daily_value': '40 %'},
    {'name': 'Potassium', 'amount': '717', 'unit': 'mg', 'daily_value': '20 %'},
    {'name': 'Total Carbohydrates',
     'amount': '47.1',
     'unit': 'g',
     'daily_value': '15 %'},
    {'name': 'Dietary Fiber',
     'amount': '6.3',
     'unit': 'g',
     'daily_value': '25 %'},
    {'name': 'Protein', 'amount': '35.6', 'unit': 'g', 'daily_value': '71 %'},
    {'name': 'Sugars', 'amount': '12', 'unit': 'g', 'daily_value': None},
    {'name': 'Vitamin A', 'amount': '855', 'unit': 'IU', 'daily_value': None},
    {'name': 'Vitamin C', 'amount': '2', 'unit': 'mg', 'daily_value': None},
    {'name': 'Calcium', 'amount': '361', 'unit': 'mg', 'daily_value': None},
    {'name': 'Iron', 'amount': '4', 'unit': 'mg', 'daily_value': None},
    {'name': 'Thiamin', 'amount': '0', 'unit': 'mg', 'daily_value': None},
    {'name': 'Niacin', 'amount': '11', 'unit': 'mg', 'daily_value': None},
    {'name': 'Vitamin B6', 'amount': '0', 'unit': 'mg', 'daily_value': None},
    {'name': 'Magnesium', 'amount': '74', 'unit': 'mg', 'daily_value': None},
    {'name': 'Folate', 'amount': '41', 'unit': 'mcg', 'daily_value': None}]
  }
  print(json.dumps(testClass.to_vegetarian(old_recipe), indent=2))
  '''
  Should return (if beef -> tofu)
  {
    "ingredients": [
      "12 whole wheat lasagna noodles",
      "1 pound lean ground tofu",
      "2 cloves garlic, chopped",
      "1/2 teaspoon garlic powder",
      "1 teaspoon dried oregano, or to taste",
      "salt and ground black pepper to taste",
      "1 (16 ounce) package cottage cheese",
      "2 eggs",
      "1/2 cup shredded Parmesan cheese",
      "1 1/2 (25 ounce) jars tomato-basil pasta sauce",
      "2 cups shredded mozzarella cheese"
    ],
    "directions": [
      "Preheat oven to 350 degrees F (175 degrees C). Watch Now",
      "Fill a large pot with lightly salted water and bring to a rolling boil over high heat. Once the water is boiling, add the lasagna noodles a few at a time, and return to a boil. Cook the pasta uncovered, stirring occasionally, until the pasta has cooked through, but is still firm to the bite, about 10 minutes. Remove the noodles to a plate. Watch Now",
      "Place the ground tofu into a skillet over medium heat, add the garlic, garlic powder, oregano, salt, and black pepper to the skillet. Cook the meat, chopping it into small chunks as it cooks, until no longer pink, about 10 minutes. Drain excess grease. Watch Now",
      "In a bowl, mix the cottage cheese, eggs, and Parmesan cheese until thoroughly combined. Watch Now",
      "Place 4 noodles side by side into the bottom of a 9x13-inch baking pan; top with a layer of the tomato-basil sauce, a layer of ground tofu mixture, and a layer of the cottage cheese mixture. Repeat layers twice more, ending with a layer of sauce; sprinkle top with the mozzarella cheese. Cover the dish with aluminum foil. Watch Now",
      "Bake in the preheated oven until the casserole is bubbling and the cheese has melted, about 30 minutes. Remove foil and bake until cheese has begun to brown, about 10 more minutes. Allow to stand at least 10 minutes before serving. Watch Now"
    ],
    ...
  }
  '''
  print("non-vegetarian recipe", json.dumps(testClass.to_non_vegetarian(old_recipe), indent=2))

  old_unhealthy_recipe = { # just made this up
    'ingredients': ['12 loaves of brioche',
                    '1 pound pork belly',
                    '2 cloves garlic, chopped',
                    '1/2 teaspoon garlic powder',
                    '1 teaspoon dried oregano, or to taste',
                    '3 tablespoons of butter',
                    'salt to taste',
                    '1 (16 ounce) package cottage cheese',
                    '2 eggs',
                    '1/2 cup shredded Parmesan cheese',
                    '1 1/2 (25 ounce) jars tomato-basil pasta sauce',
                    '2 cups shredded mozzarella cheese'],
    'directions': ['Preheat oven to 350 degrees F (175 degrees C).\n                                    Watch Now',
                   'Fill a large pot with lightly salted water and bring to a rolling boil over high heat. Once the water is boiling, add the loaves of bread a few at a time, and return to a boil. Cook the pasta uncovered, stirring occasionally, until the pasta has cooked through, but is still firm to the bite, about 10 minutes. Remove the noodles to a plate.\n                                    Watch Now',
                   'Place the chopped pork belly into a skillet over medium heat, add the garlic, garlic powder, oregano, salt, and black pepper to the skillet. Cook the meat, chopping it into small chunks as it cooks, until no longer pink, about 10 minutes. Drain excess grease.\n                                    Watch Now',
                   'In a bowl, mix the cottage cheese, eggs, and Parmesan cheese until thoroughly combined.\n                                    Watch Now',
                   'Place 4 noodles side by side into the bottom of a 9x13-inch baking pan; top with a layer of the tomato-basil sauce, a layer of ground beef mixture, and a layer of the cottage cheese mixture. Repeat layers twice more, ending with a layer of sauce; sprinkle top with the mozzarella cheese. Cover the dish with aluminum foil.\n                                    Watch Now',
                   'Bake in the preheated oven until the casserole is bubbling and the cheese has melted, about 30 minutes. Remove foil and bake until cheese has begun to brown, about 10 more minutes. Allow to stand at least 10 minutes before serving.\n                                    Watch Now'],
    'nutrition': [{'name': 'Total Fat',
                   'amount': '19.3',
                   'unit': 'g',
                   'daily_value': '30 %'},
                  {'name': 'Saturated Fat', 'amount': '9.0', 'unit': 'g', 'daily_value': None},
                  {'name': 'Cholesterol',
                   'amount': '115',
                   'unit': 'mg',
                   'daily_value': '38 %'},
                  {'name': 'Sodium', 'amount': '999', 'unit': 'mg', 'daily_value': '40 %'},
                  {'name': 'Potassium', 'amount': '717', 'unit': 'mg', 'daily_value': '20 %'},
                  {'name': 'Total Carbohydrates',
                   'amount': '47.1',
                   'unit': 'g',
                   'daily_value': '15 %'},
                  {'name': 'Dietary Fiber',
                   'amount': '6.3',
                   'unit': 'g',
                   'daily_value': '25 %'},
                  {'name': 'Protein', 'amount': '35.6', 'unit': 'g', 'daily_value': '71 %'},
                  {'name': 'Sugars', 'amount': '12', 'unit': 'g', 'daily_value': None},
                  {'name': 'Vitamin A', 'amount': '855', 'unit': 'IU', 'daily_value': None},
                  {'name': 'Vitamin C', 'amount': '2', 'unit': 'mg', 'daily_value': None},
                  {'name': 'Calcium', 'amount': '361', 'unit': 'mg', 'daily_value': None},
                  {'name': 'Iron', 'amount': '4', 'unit': 'mg', 'daily_value': None},
                  {'name': 'Thiamin', 'amount': '0', 'unit': 'mg', 'daily_value': None},
                  {'name': 'Niacin', 'amount': '11', 'unit': 'mg', 'daily_value': None},
                  {'name': 'Vitamin B6', 'amount': '0', 'unit': 'mg', 'daily_value': None},
                  {'name': 'Magnesium', 'amount': '74', 'unit': 'mg', 'daily_value': None},
                  {'name': 'Folate', 'amount': '41', 'unit': 'mcg', 'daily_value': None}]
  }
  print("unhealthy recipe", json.dumps(testClass.to_healthy(old_unhealthy_recipe), indent=2))
  '''
  should:
  - replace pork belly with tofu
  - halve the sugar content
  - leave salt ingredient unchanged with no error
  - replace bread with gluten free bread
  '''

  old_healthy_recipe = {  # just made this up
      'ingredients': ['1 cup of brown rice',
                      '1 pound of turkey bacon',
                      '2 cloves garlic, chopped',
                      '1/2 teaspoon garlic powder',
                      '1 teaspoon dried oregano, or to taste',
                      '3 tablespoons of butter',
                      'salt to taste',
                      '1 (16 ounce) package cottage cheese',
                      '2 eggs',
                      '1/2 cup shredded Parmesan cheese',
                      '1 1/2 (25 ounce) jars tomato-basil pasta sauce'],
      'directions': ['Preheat oven to 350 degrees F (175 degrees C).\n                                    Watch Now',
                     'Fill a large pot with lightly salted water and bring to a rolling boil over high heat. Once the water is boiling, add the brown rice a cup at a time, and return to a boil. Cook the pasta uncovered, stirring occasionally, until the pasta has cooked through, but is still firm to the bite, about 10 minutes. Remove the noodles to a plate.\n                                    Watch Now',
                     'Place the chopped turkey bacon into a skillet over medium heat, add the garlic, garlic powder, oregano, salt, and black pepper to the skillet. Cook the meat, chopping it into small chunks as it cooks, until no longer pink, about 10 minutes. Drain excess grease.\n                                    Watch Now',
                     'In a bowl, mix the cottage cheese, eggs, and Parmesan cheese until thoroughly combined.\n                                    Watch Now',
                     'Place 4 noodles side by side into the bottom of a 9x13-inch baking pan; top with a layer of the tomato-basil sauce, a layer of ground beef mixture, and a layer of the cottage cheese mixture. Repeat layers twice more, ending with a layer of sauce; sprinkle top with the mozzarella cheese. Cover the dish with aluminum foil.\n                                    Watch Now',
                     'Bake in the preheated oven until the casserole is bubbling and the cheese has melted, about 30 minutes. Remove foil and bake until cheese has begun to brown, about 10 more minutes. Allow to stand at least 10 minutes before serving.\n                                    Watch Now'],
      'nutrition': [{'name': 'Total Fat',
                     'amount': '19.3',
                     'unit': 'g',
                     'daily_value': '30 %'},
                    {'name': 'Saturated Fat', 'amount': '9.0', 'unit': 'g', 'daily_value': None},
                    {'name': 'Cholesterol',
                     'amount': '115',
                     'unit': 'mg',
                     'daily_value': '38 %'},
                    {'name': 'Sodium', 'amount': '999', 'unit': 'mg', 'daily_value': '40 %'},
                    {'name': 'Potassium', 'amount': '717', 'unit': 'mg', 'daily_value': '20 %'},
                    {'name': 'Total Carbohydrates',
                     'amount': '47.1',
                     'unit': 'g',
                     'daily_value': '15 %'},
                    {'name': 'Dietary Fiber',
                     'amount': '6.3',
                     'unit': 'g',
                     'daily_value': '25 %'},
                    {'name': 'Protein', 'amount': '35.6', 'unit': 'g', 'daily_value': '71 %'},
                    {'name': 'Sugars', 'amount': '12', 'unit': 'g', 'daily_value': None},
                    {'name': 'Vitamin A', 'amount': '855', 'unit': 'IU', 'daily_value': None},
                    {'name': 'Vitamin C', 'amount': '2', 'unit': 'mg', 'daily_value': None},
                    {'name': 'Calcium', 'amount': '361', 'unit': 'mg', 'daily_value': None},
                    {'name': 'Iron', 'amount': '4', 'unit': 'mg', 'daily_value': None},
                    {'name': 'Thiamin', 'amount': '0', 'unit': 'mg', 'daily_value': None},
                    {'name': 'Niacin', 'amount': '11', 'unit': 'mg', 'daily_value': None},
                    {'name': 'Vitamin B6', 'amount': '0', 'unit': 'mg', 'daily_value': None},
                    {'name': 'Magnesium', 'amount': '74', 'unit': 'mg', 'daily_value': None},
                    {'name': 'Folate', 'amount': '41', 'unit': 'mcg', 'daily_value': None}]
  }
  print("unhealthy recipe", json.dumps(testClass.to_unhealthy(old_healthy_recipe), indent=2))
  '''
  should:
  - replace brown rice with white rice
  - double the butter content
  - leave salt ingredient unchanged with no error
  - replace cottage cheese with mozzarella
  '''

