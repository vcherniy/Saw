from saw.parsers import Parser
from item import Item
from items import Items


class Saw:
    @staticmethod
    def load(text):
        return Parser.load_all(text)