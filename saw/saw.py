#from item import Item
#from items import Items
#from saw.parsers.paragraphs import Paragraphs, Parser


class Saw:
    @staticmethod
    def load(text):
        saw = Item()
        Paragraphs.load(saw, text)
        return saw