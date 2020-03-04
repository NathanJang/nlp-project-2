from recipeFetcher import RecipeFetcher
from word_transformations import Transformer
from nlp_common import WordTagger

import user_prompts


def run_nlp(recipe):
  tagger = WordTagger()

  tagger.process_ingredients(recipe)
  tagger.process_tools(recipe)
  tagger.process_recipe_methods(recipe)
  tagger.process_directions(recipe)
  # todo? do we want to return tagger class object or return dict
  return tagger


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
  run_nlp(recipe)
  # transformation recipe
  new_recipe = transform_recipe(recipe)
  run_nlp(new_recipe)


if __name__ == '__main__':
  main()