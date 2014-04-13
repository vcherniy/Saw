from saw.parsers.sentences import Parser, Sentences


class Paragraphs(Parser):
    _type = 'paragraphs'
    _child_class = Sentences

    @classmethod
    def parse(cls, text):
        items = text.split("\n")
        result, tmp = [], []
        for item in items:
            if item != '':
                result.append(tmp)
                result.append(item.strip())
                tmp = []
            tmp.append("\n")
        # end of string will add \n. We should ignore it.
        tmp.pop()
        result.append(tmp)
        return result