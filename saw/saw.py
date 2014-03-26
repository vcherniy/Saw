#from item import Item
#from items import Items
#from saw.parsers.paragraphs import Paragraphs, Parser


class Saw:
    @staticmethod
    def load(text):
        return Paragraphs.load(Item(), text)