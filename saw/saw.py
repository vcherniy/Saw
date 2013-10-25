from parsers import Parse
from item import Item
from items import Items

class Saw:
    def load(self, text):
        return Parse.load(text)