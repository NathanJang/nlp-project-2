from recipeFetcher import RecipeFetcher
from word_transformations import Transformer
from nlp_common import WordTagger
from displayResults import DisplayResults

import user_prompts


def run_nlp(recipe):
  """Takes recipe array and returns nlp processed results

  :param recipe:
  :return:
  """
  tagger = WordTagger()

  tagger.process_ingredients(recipe)
  tagger.process_tools(recipe)
  tagger.process_recipe_methods(recipe)
  tagger.process_directions(recipe)

  return {
    'ingredients': tagger.found_ingredients,
    'tools': tagger.found_tools,
    'methods': tagger.found_methods,
    'directions': tagger.process_directions
  }


def get_recipe():
  """prompts a user for a url, searches and parses a recipe and returns dict representation of a recipe.

  :return: {}, recipe json
  """
  rf = RecipeFetcher()
  recipe_url = user_prompts.search_url_input()
  return rf.scrape_recipe(recipe_url)


def transform_recipe(recipe):
  """prompt and perform transformations on a recipe using the transformation mapping in the class

  :param recipe: recipe to perform transformations on
  :return: {}, new recipe
  """
  transformer = Transformer()
  user_prompts.set_transformations()
  trans_option = user_prompts.transformation()
  transformed_recipe = transformer.transformation_mapping[trans_option](recipe)
  return transformed_recipe


def main():
  recipe = get_recipe()
  nlp_recipe_results = run_nlp(recipe)
  printer = DisplayResults(results=nlp_recipe_results)
  printer.print_all()

  # transformation recipe
  new_recipe = transform_recipe(recipe)
  transformed_nlp_results = run_nlp(new_recipe)
  printer = DisplayResults(results=transformed_nlp_results)
  printer.print_all()
  # todo: keep transforming
  user_prompts.continue_startover()
  user_prompts.next_step()

if __name__ == '__main__':
  main()
