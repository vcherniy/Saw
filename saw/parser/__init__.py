from .paragraphs import Paragraphs

class Parse:
    def __init__(self):
        saw = Saw_Items()
        Paragraphs.load(saw, text)
        return saw