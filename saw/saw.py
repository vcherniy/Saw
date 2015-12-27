from parsers.paragraphs import Paragraphs, Sentences
from parsers.blocks import Blocks, Words


class Saw:
    paragraphs = Paragraphs
    sentences = Sentences
    blocks = Blocks
    words = Words

    @staticmethod
    def load(text):
        return Paragraphs.load(text)