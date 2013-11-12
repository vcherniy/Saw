from saw.parsers.sentences import Sentences


class Paragraphs(Parser):
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
        # end of string will add \n. We should ignore it.
        tmp.pop()
        if tmp:
            result.append(tmp)
        return result