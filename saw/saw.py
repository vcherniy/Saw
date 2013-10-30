from parsers import Parse
from item import Item
from items import Items

class Saw:
    @staticmethod
    def load(text):
        return Parse.load(text)