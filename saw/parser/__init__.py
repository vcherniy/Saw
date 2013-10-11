from .paragraphs import Paragraphs
from ..saw import Items

class Parse:
    def load(self, text):
        saw = Items()
        Paragraphs.load(saw, text)
        return saw