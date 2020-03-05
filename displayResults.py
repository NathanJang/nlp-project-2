class DisplayResults:
  def __init__(self, results):
    self.results = results
    print('NLP RESULTS\n\n')

  '''
  More like the latter where you have dictionaries indicating the presence of certain tools, methods, 
  and times (e.g., preheat oven to 350F and bake x for 50 minutes). When displaying the step, 
  you can simply highlight these elements in the sentence (preheat *oven* to 350F 
  and *bake x* for *50 minutes*) or add some sort of structured summary by the end of 
  the sentence (ingredient: x, tool: oven, method: baking, time: 50 min). However you choose, 
  make sure you keep track of this information.
  
  '''

  def print_steps(self):
    [print(raw_step) for raw_step in self.results['directions']['raw']]
    print('\n\n')

    for direction, cleaned_step in self.results['directions']['cleaned'].items():
      step_string = f'{direction}: '
      if cleaned_step['ingredients']:
        step_string += ' INGREDIENTS: ' + ', '.join(cleaned_step['ingredients'])

      if cleaned_step['methods']:
        step_string += ' METHODS: ' + ', '.join(cleaned_step['methods'])

      if cleaned_step['tools']:
        step_string += ' TOOLS: ' + ', '.join(cleaned_step['tools'])

      if cleaned_step['times']:
        step_string += ' TIMES: ' + ', '.join(cleaned_step['times'])

      step_string += '\n'
      print(step_string)
    print('\n\n')

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
    self.print_steps()
