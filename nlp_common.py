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
    pass


  def process_ingredients(self, recipe_results):
    # todo: may need to limit list of ingredients
    raw_ingredients = recipe_list['ingredients']
    MEASUREMENTS = WL.get_words('measurements')
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
        if fragment in MEASUREMENTS:
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
        msr_check = fragment != ingredient_info['measurement'] and fragment not in MEASUREMENTS and fragment + 's' not in MEASUREMENTS
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

if __name__ == '__main__':
  rf = RecipeFetcher()
  meat_lasagna = rf.search_recipes('meat lasagna')[0]
  recipe_list = rf.scrape_recipe(meat_lasagna)
  tagger = WordTagger()
  tagger.process_ingredients(recipe_list)
