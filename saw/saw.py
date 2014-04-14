from parsers.paragraphs import Paragraphs


class Saw:
    @staticmethod
    def load(text):
        return Paragraphs.load(text)