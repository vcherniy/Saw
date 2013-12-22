from saw.parsers import Parser
from saw.parsers import Item


class Words(Parser):
    _type = 'words'

    @staticmethod
    def parse(text):
        return [x.strip() for x in text.split(' ') if x != '']

    @staticmethod
    def _process_string(saw, text):
        _item = Item()
        _item.text_append(text)
        saw.children.append(_item)

    @classmethod
    def _load_children(cls, saw, data):
        for i in range(0, len(data), 1):
            cls._process_string(saw, data[i])