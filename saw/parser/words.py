import base

class Words(base.Base):
    _type = 'words'
    child_class = None

    @staticmethod
    def parse(text):
        return [x.strip() for x in text.split(' ') if x != '']

    @staticmethod
    def repr(obj):
        return ''