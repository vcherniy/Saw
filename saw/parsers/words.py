from saw.parsers import Parser, Node


class Words(Parser):
    _type = 'words'

    @classmethod
    def parse(cls, text):
        return [x.strip() for x in text.split(' ') if x != '']

    @classmethod
    def process_mods(cls, data):
        return data

    @classmethod
    def _load_children(cls, saw, data):
        for x in data:
            saw.append(Node().text(x))