
MEASUREMENT_MAPPING = {
  "pound": "lb",
  "pounds": "lbs",
  "grams": "g",
  "kilogram": "kg",
  "kilograms": "kgs",
  "ounces": "oz",
  "ounce": "oz"
}


def convert_measurements(measurement):
  msr = measurement.lower()
  try:
    return MEASUREMENT_MAPPING[msr]
  except KeyError:
    return msr


def get_meal_name(recipe_url):
  split_url = recipe_url.split('/')
  split_name = split_url[recipe_url.index('recipe') + 2].split('-')
  return ' '.join([word.lower().capitalize() for word in split_name])

