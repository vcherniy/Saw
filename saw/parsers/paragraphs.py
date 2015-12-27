from saw.parsers.sentences import Parser, Sentences


class Paragraphs(Parser):
    _child_class = Sentences

    @classmethod
    def parse(cls, text):
        items = text.split("\n")
        result, tmp = [], []
        for item in items:
            _item = item.strip()
            if _item != '':
                result.append(tmp)
                result.append(_item)
                tmp = []
            tmp.append("\n")
        # end of string will add \n. We should ignore it.
        tmp.pop()
        result.append(tmp)
        return result
