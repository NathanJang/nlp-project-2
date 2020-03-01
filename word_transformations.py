import json

class WordLists():

  def __init__(self):
    self.words_file_name = 'word_list.json'

    with open(self.words_file_name, 'r') as words_file:
      self.words_json = json.load(words_file)

  def get_words(self, word):
    return self.words_json[word]

testClass = WordLists()
