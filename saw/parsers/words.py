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
    def _process_string(cls, saw, text, to_before):
        saw.append(Node('').text(text))

    @classmethod
    def _load_children(cls, saw, data):
        for i in range(0, len(data)):
            cls._process_string(saw, data[i], [])