import base
from blocks import Blocks

class Sentences(base.Base):
    _type = 'sentences'
    child_class = Blocks

    @staticmethod
    def parse(text):
        # x.extend(
        return text.split('.')