import base
from words import Words

class Blocks(base.Base):
    _type = 'blocks'
    child_class = Words

    @staticmethod
    def parse(text):
        return text.split(',')