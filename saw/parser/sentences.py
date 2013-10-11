from base import Base
from blocks import Blocks

class Sentences(Base):
    _type = 'sentences'
    child_class = Blocks

    @staticmethod
    def parse(text):
        # x.extend(
        return text.split('.')