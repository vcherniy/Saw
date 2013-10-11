from base import Base
from sentences import Sentences

class Paragraphs(Base):
    _type = 'paragraphs'
    child_class = Sentences

    @staticmethod
    def parse(text):
        return [text]