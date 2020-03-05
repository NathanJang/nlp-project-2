import nltk
from word_transformations import Transformer
from recipeFetcher import RecipeFetcher

from fractions import Fraction

STOP_WORDS = {
  'ingredients': ['taste', 'tastes', 'and', 'oven']
}

PASS_WORDS = {
  'ingredients': []
}

transformer = Transformer()

# TODO: MAJOR:
# improve ingredient parsing and measurements


class WordTagger:
  def __init__(self):
    self.measurements = transformer.__getitem__('measurements')
    self.tools = transformer.__getitem__('tools')
    self.times = transformer.__getitem__('duration')
    self.methods = transformer.__getitem__('cookingMethods')
    # store recipe data in class to access at any time
    # todo: move this to a base list for ingredients
    self.found_ingredients = {}
    self.found_methods = None
    self.found_tools = None
    self.found_directions = None

  def process_ingredients(self, recipe_results):
    # todo: may need to limit list of ingredients
    raw_ingredients = recipe_results['ingredients']
    processed_ingredients = self.found_ingredients

    for ing in raw_ingredients:
      ingredient_info = {
        'name': '',
        'qty': 0,
        'measurement': '',
        'info': '',
        'paren': '',
      }

      split_words = ing.split()

      for fragment in split_words:
        # get the quantity from the recipe
        if '/' in fragment and '(' not in fragment:
          ingredient_info['qty'] += float(sum(Fraction(part) for part in fragment.split()))
        if fragment.isdigit():
          try:
            ingredient_info['qty'] += float(fragment)
          except ValueError:
            pass

        # get measurement from recipe
        if fragment in self.measurements or f'{fragment}s' in self.measurements:
          ingredient_info['measurement'] = fragment

        if '(' in fragment:
          split_ingredient_fragments = ing.split()
          ing_ind = split_ingredient_fragments.index(fragment)
          ing_ind_2 = ''
          if ')' in split_ingredient_fragments[ing_ind]:
            ing_ind_2 = ing_ind + 1
          if ing_ind_2 == ing_ind + 1:
            ingredient_info['paren'] = ' '.join(str(part) for part in split_ingredient_fragments[ing_ind:ing_ind_2 + 1])

        # get the ingredients and description
        qty_check = fragment != ingredient_info['qty'] and not fragment.isdigit()
        msr_check = fragment != ingredient_info['measurement'] and fragment not in self.measurements \
                    and fragment + 's' not in self.measurements
        parens_check = '(' not in fragment and ')' not in fragment
        if qty_check and msr_check and parens_check:
          # use nltk to tag the parts of speach
          tagged_tokens = nltk.pos_tag(fragment.split())
          fragment_word = tagged_tokens[0][0]
          fragment_pos = tagged_tokens[0][1]

          # todo: move these codes to constants
          # assign ingredient and description based on fragment
          if fragment_word not in STOP_WORDS and (fragment_pos in ["NN", "NNS"] or fragment_word in PASS_WORDS):
            ingredient_info['name'] += f'{fragment} '

          if fragment_word not in ingredient_info['name'] and fragment_pos in ["JJ", "VBN", "RB"]:
            ingredient_info['info'] += f'{fragment} '

      # some clean up :)
      if ingredient_info['qty'] == 0:
        ingredient_info['qty'] = ""
      ingredient_info['name'] = ingredient_info['name'].strip()
      ingredient_info['info'] = ingredient_info['info'].strip()

      processed_ingredients[ing] = ingredient_info

    self.found_ingredients = processed_ingredients
    return processed_ingredients

  def process_tools(self, recipe_results):
    raw_directions = recipe_results['directions']
    processed_tools = []

    for direction in raw_directions:
      for word in direction.split():
        cleaned_word = word.strip(',.').lower()
        if cleaned_word not in processed_tools and (cleaned_word in self.tools or f'{cleaned_word}s' in self.tools):
          processed_tools.append(cleaned_word)

    self.found_tools = processed_tools
    return processed_tools

  def process_recipe_methods(self, recipe_results):
    raw_directions = recipe_results['directions']
    processed_methods = []
    # todo: optimize redundant code.
    for direction in raw_directions:
      for word in direction.split():
        cleaned_word = word.strip(',.').lower()
        if cleaned_word not in processed_methods and (
            cleaned_word in self.methods or f'{cleaned_word}ing' in self.methods):
          processed_methods.append(cleaned_word)

    self.found_methods = processed_methods
    return processed_methods

  def process_directions(self, recipe_results):
    raw_directions = recipe_results['directions']
    direction_list = []
    found_directions = {}
    processed_directions = {}
    cnt = 1
    # todo: differentiate between extra (you might like) recipes and directions
    for direction in raw_directions:
      if len(direction.split()) > 2:
        split_direction = direction.split('.')
        new_direction = [chunk for chunk in split_direction if len(chunk) > 0]
        direction_list.extend(new_direction)

    for direction in raw_directions:
      cleaned_direction = direction.lower().split()
      if len(cleaned_direction) > 2:
        direction_name = f"direction_{cnt}"
        found_directions.update({direction_name:
                                   {"ingredients": [],
                                    "methods": [],
                                    "times": [],
                                    "tools": []
                                    }})

        for ind in range(len(cleaned_direction)):
          # todo: maybe don't modify the main cleaned_direction variable
          cleaned_direction[ind] = cleaned_direction[ind].strip(',.')
          for ingredient in self.found_ingredients:
            ingredient_name = self.found_ingredients[ingredient]['name']
            # todo: move this to a helper function to cut down on code
            len_check = len(cleaned_direction[ind]) > 2 and not cleaned_direction[ind].isdigit() and \
                        cleaned_direction[ind] not in STOP_WORDS['ingredients']
            ingredient_check = cleaned_direction[ind] in ingredient_name or f'{cleaned_direction[ind]}s' in \
                               ingredient_name or cleaned_direction[ind][:-1] in ingredient_name
            ing_check = cleaned_direction[ind] not in found_directions[direction_name]["ingredients"]
            # add ingredient to found directions for specific direction
            if ingredient_check and ing_check and len_check:
              found_directions[direction_name]["ingredients"].append(cleaned_direction[ind])
          # todo: maybe change to elif
          # add tools to found directions for specific direction
          tool_check = cleaned_direction[ind] in self.found_tools or f'{cleaned_direction[ind]}s' in \
                       self.found_tools or cleaned_direction[ind][:-1] in self.found_tools
          t_check = cleaned_direction[ind] not in found_directions[direction_name]['tools']
          if tool_check and t_check:
            found_directions[direction_name]["tools"].append(cleaned_direction[ind])

          # add methods to found directions for specific direction
          method_check = cleaned_direction[ind] in self.found_methods or f'{cleaned_direction[ind]}s' in \
                         self.found_methods or cleaned_direction[ind][:-1] in self.found_tools
          m_check = cleaned_direction[ind] not in found_directions[direction_name]['methods']
          if method_check and m_check:
            found_directions[direction_name]["methods"].append(cleaned_direction[ind])

          # add timing
          # TIMING METHOD 1
          if cleaned_direction[ind] == 'degrees':
            cln_degrees = []
            if cleaned_direction[ind - 1].strip('()').isdigit():
              cln_degrees.append(cleaned_direction[ind - 1])
            if len(cleaned_direction[ind+1].strip("().")) == 1:
              cln_degrees.append(cleaned_direction[ind + 1])

            deg_str = ' degrees '.join(cln_degrees).strip("().")
            found_directions[direction_name]["times"].append(deg_str)

          # TIMING METHOD 2
          time_check = cleaned_direction[ind] in self.times or f'{cleaned_direction[ind]}s' in \
                         self.times or cleaned_direction[ind][:-1] in self.times
          tm_check = cleaned_direction[ind] not in found_directions[direction_name]['times']
          # todo: fix duplicate timings being inserted when theyre fragmented
          if time_check and tm_check:
            temp_count = 1
            time_str = cleaned_direction[ind]
            while True:
              if cleaned_direction[ind - temp_count].isdigit() or cleaned_direction[ind - temp_count] == "to":
                time_str = f'{cleaned_direction[ind - temp_count]} {time_str}'
              else:
                break
              temp_count += 1
              if time_str not in found_directions[direction_name]['times']:
                found_directions[direction_name]["times"].append(time_str)

          # todo: remove similar time duplicates asap!!
          # sorted_times = sorted(found_directions[direction_name]["times"])
          # found_directions[direction_name]["times"] = list(sorted_times)

        cnt += 1

    processed_directions.update({"raw": direction_list})
    processed_directions.update({"cleaned": found_directions})
    self.found_directions = direction_list
    return processed_directions

if __name__ == '__main__':
  rf = RecipeFetcher()
  recipe_url = 'https://www.allrecipes.com/recipe/22776/restaurant-style-lasagna/?internalSource=previously%20viewed&referringContentType=Homepage&clickId=cardslot%2040'
  # found_recipe = rf.search_recipes(recipe_search_text)[0]
  recipe = rf.scrape_recipe(recipe_url)
  tagger = WordTagger()
  tagger.process_ingredients(recipe)
  tagger.process_tools(recipe)
  tagger.process_recipe_methods(recipe)
  tagger.process_directions(recipe)

