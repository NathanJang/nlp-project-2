from bs4 import BeautifulSoup
import string
import requests
import re

class RecipeFetcher:
  search_base_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'
  # todo: move to constants
  units = {}

  def search_recipes(self, keywords):
    search_url = self.search_base_url % (keywords.replace(' ', '+'))

    page_html = requests.get(search_url)
    page_graph = BeautifulSoup(page_html.content)

    return [recipe.a['href'] for recipe in \
            page_graph.find_all('div', {'class': 'grid-card-image-container'})]

  def scrape_recipe(self, recipe_url):
    results = {}

    page_html = requests.get(recipe_url)
    page_graph = BeautifulSoup(page_html.content)

    results['ingredients'] = [ingredient.text for ingredient in \
                              page_graph.find_all('span', {'itemprop': 'recipeIngredient'})]

    results['directions'] = [direction.text.strip() for direction in \
                             page_graph.find_all('span', {'class': 'recipe-directions__list--item'})
                             if direction.text.strip()]

    results['nutrition'] = self.scrape_nutrition_facts(recipe_url)

    return results

  def scrape_nutrition_facts(self, recipe_url):
    results = []

    nutrition_facts_url = '%s/fullrecipenutrition' % (recipe_url)

    page_html = requests.get(nutrition_facts_url)
    page_graph = BeautifulSoup(page_html.content)

    nutrition_rows = page_graph.find_all('div', {'class': 'nutrition-row'})

    r = re.compile("([0-9]*\.?[0-9]*)([a-zA-Z]+)")

    for nutrient_row in nutrition_rows:
      # todo: clean up sanitize and strip
      nutrient = {}
      nutrient_row_children = nutrient_row.text.split(':')
      nutrient['name'] = nutrient_row_children[0].strip()
      split_amount_and_value = nutrient_row_children[1].split('\n')

      # extract unit and amount
      nutrient['amount'] = self.extract_numbers(split_amount_and_value[0])
      nutrient['unit'] = self.extract_unit(split_amount_and_value[0])

      # nutrient['daily value'] = split_amount_and_value[1].split(' ')[0] or '0'
      nutrient['daily value'] = split_amount_and_value[1] or None

      # strip all new lines from our values
      nutrient = {key: val.strip() if val is not None else None for key, val in nutrient.items()}

      results.append(nutrient)
    print(results)
    return results

  def extract_numbers(self, text):
    try:
      return re.findall(r"\d+\.\d+|\d+", text)[0]
    except IndexError:
      return 0

  def extract_unit(self, text):
    try:
      return re.split(r"\d+\.\d+|\d+", text)[1]
    except IndexError:
      return ''


rf = RecipeFetcher()
meat_lasagna = rf.search_recipes('meat lasagna')[0]
results = rf.scrape_recipe(meat_lasagna)

"""
Should return:

{'ingredients': ['12 whole wheat lasagna noodles',
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
  {'name': 'Folate', 'amount': '41', 'unit': 'mcg', 'daily_value': None}]}
"""