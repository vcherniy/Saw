from ..saw import Items

class Base:
    @classmethod
    def load(self, saw, text):
        #if not (self._type in saw.__dict__):
        #    saw.__dict__[ self._type ] = list()

        items = self.parse(text)
        for item in items:

            if isinstance(item, list):
                pass
            elif self.child_class:
                item = self.child_class.load( list(), item)
            # else pass
            saw.append(item)
        return saw

from paragraphs import Paragraphs

class Parse:
    @staticmethod
    def load(text):
        saw = list()
        Paragraphs.load(saw, text)
        return saw