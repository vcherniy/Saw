import base
from sentences import Sentences

class Paragraphs(base.Base):
    _type = 'paragraphs'
    child_class = Sentences

    @staticmethod
    def parse(text):
        return [text]