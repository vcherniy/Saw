from saw.parsers import Parser


class Words(Parser):
    _type = 'words'
    child_class = None

    @staticmethod
    def parse(text):
        return [x.strip() for x in text.split(' ') if x != '']