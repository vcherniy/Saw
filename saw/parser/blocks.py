from base import Base
from words import Words

class Blocks(Base):
    _type = 'blocks'
    child_class = Words

    @staticmethod
    def parse(text):
        return text.split(',')