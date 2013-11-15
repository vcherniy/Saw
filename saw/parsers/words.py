from saw.parsers import Parser


class Words(Parser):
    _type = 'words'

    @staticmethod
    def parse(text):
        return [x.strip() for x in text.split(' ') if x != '']

    @classmethod
    def _process_mods(cls, data):
        return data