
class DisplayResults():
  def __init__(self, results):
    self.results = results

  def print_steps(self):
    steps_string = f'ingredients: {self.results["ingredients"]}'
    print(steps_string)
