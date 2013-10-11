from ..saw import Items

class Base:
    @classmethod
    def load(self, saw, text):
        if not (self._type in saw.__dict__):
            saw.__dict__[ self._type ] = Items()

        items = self.parse(text)
        for item in items:
            if item == '':
                continue
            if self.child_class:
                item = self.child_class.load( Items(), item)
            saw.__dict__[ self._type ].append(item)
        return saw

from paragraphs import Paragraphs

class Parse:
    @staticmethod
    def load(text):
        saw = Items()
        Paragraphs.load(saw, text)
        return saw