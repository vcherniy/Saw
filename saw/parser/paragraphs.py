import base
from sentences import Sentences

class Paragraphs(base.Base):
    _type = 'paragraphs'
    child_class = Sentences

    @staticmethod
    def parse(text):
        items = text.split("\n")
        result, tmp = [], []
        for item in items:
            if item != '':
                if tmp:
                    result.append(tmp)
                    tmp = []
                result.append(item.strip())
            tmp.append("\n")
        tmp.pop()
        if tmp:
            result.append(tmp)
        return result