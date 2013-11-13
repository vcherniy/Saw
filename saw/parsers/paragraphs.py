from saw.parsers.sentences import Parser, Sentences


class Paragraphs(Parser):
    _type = 'paragraphs'
    _child_class = Sentences

    @staticmethod
    def parse(text):
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
        if not tmp:
            tmp = []
        result.append(tmp)
        return result