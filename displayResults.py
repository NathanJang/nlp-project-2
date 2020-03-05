class DisplayResults:
  def __init__(self, results):
    self.results = results
    print('NLP RESULTS\n\n')

  def print_steps(self):
    steps_string = f'ingredients: {self.results["ingredients"]}'
    print(steps_string)

  def print_key(self, key):
    [print(f'{key}: {i}') for i in self.results[key]]
    print('\n\n')

  def print_ingredients(self):
    for ingredient, json in self.results['ingredients'].items():
      string = f'raw ingredient: {ingredient}, parsed ingredient: {json["name"]}, '
      if json['paren']:
        string += f'{json["paren"]} '
      if json['qty'] or json['measurement']:
        string += f'qty: {json["qty"]} {json["measurement"]} '
      if json['info']:
        string += f'{json["info"]}'
      print(string)
    print('\n\n')

  def print_all(self):
    self.print_key('tools')
    self.print_key('methods')
    self.print_ingredients()
