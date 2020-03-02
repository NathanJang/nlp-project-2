import nltk
from word_transformations import WordLists
from recipeFetcher import RecipeFetcher

from fractions import Fraction
STOP_WORDS = {
  'ingredients': ['taste', 'tastes']
}

PASS_WORDS = {
  'ingredients': []
}

WL = WordLists()


class WordTagger:
  def __init__(self):
    self.measurements = WL.get_words('measurements')
    self.tools = WL.get_words('tools')

  def process_ingredients(self, recipe_results):
    # todo: may need to limit list of ingredients
    raw_ingredients = recipe_list['ingredients']
    processed_ingredients = {}

    for ing in raw_ingredients:
      ingredient_info = {
        'ingredient': '',
        'qty': 0,
        'measurement': '',
        'weight': '',
        'descrip': '',
        'paren': '', # todo change this
      }

      split_words = ing.split()

      for fragment in split_words:
        # get the quantity from the recipe
        if '/' in fragment and '(' not in fragment:
          ingredient_info['qty'] = float(sum(Fraction(s) for s in fragment.split()))
        else:
          try:
            ingredient_info['qty'] = float(fragment)
          except ValueError:
            pass

        # get measurement from recipe
        if fragment in self.measurements:
          ingredient_info['measurement'] = fragment

        if '(' in fragment:
          split_ingredient_fragments = ing.split()
          ing_ind = split_ingredient_fragments.index(fragment)
          ing_ind_2 = ''
          if ')' in split_ingredient_fragments[ing_ind + 1]:
            ing_ind_2 = ing_ind + 1
          if ing_ind_2 == ing_ind + 1:
            ingredient_info['paren'] = ' '.join(str(m) for m in split_ingredient_fragments[ing_ind:ing_ind_2+1])

        # get the ingredients and description
        qty_check = fragment != ingredient_info['qty'] and not fragment.isdigit()
        msr_check = fragment != ingredient_info['measurement'] and fragment not in self.measurements \
                    and fragment + 's' not in self.measurements
        parens_check = '(' not in fragment or ')' not in fragment
        if qty_check and msr_check and parens_check:
          # use nltk to tag the parts of speach
          tagged_tokens = nltk.pos_tag(fragment.split())
          fragment_word = tagged_tokens[0][0]
          fragment_pos = tagged_tokens[0][1]

          # assign ingredient and description based on fragment
          if fragment_word not in STOP_WORDS and (fragment_pos in ["NN", "NNS"] or fragment_word in PASS_WORDS):
            ingredient_info['ingredient'] += f'{fragment} '

          if fragment_word not in ingredient_info['ingredient'] and fragment_pos in ["JJ", "VBN", "RB"]:
            ingredient_info['descrip'] += f'{fragment} '

        # todo: maybe remove this
        if ingredient_info['qty'] == 0:
          ingredient_info['qty'] = ""

      processed_ingredients[ing] = ingredient_info
    print(processed_ingredients)
    return processed_ingredients

  def process_tools(self, recipe_results):
    raw_directions = recipe_results['directions']
    processed_tools = []

    for direction in raw_directions:
      for word in direction.split():
        cleaned_word = word.strip(',.').lower()
        if cleaned_word not in processed_tools and (cleaned_word in self.tools or f'{cleaned_word}s' in self.tools):
          processed_tools.append(cleaned_word)

    return processed_tools

  def process_recipe_methods(self, recipe_results):
    raw_directions = recipe_results['directions']
    methods = WL.get_words('methods')
    processed_methods = []
    # todo: optimize redundant code.
    for direction in raw_directions:
      for word in direction.split():
        cleaned_word = word.strip(',.').lower()
        if cleaned_word not in processed_methods and (cleaned_word in methods or f'{cleaned_word}ing' in methods):
          processed_methods.append(cleaned_word)

    return processed_methods

  def process_steps(self):

if __name__ == '__main__':
  rf = RecipeFetcher()
  meat_lasagna = rf.search_recipes('meat lasagna')[0]
  recipe_list = rf.scrape_recipe(meat_lasagna)
  tagger = WordTagger()
  tagger.process_ingredients(recipe_list)
