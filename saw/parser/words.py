from base import Base

class Words(Base):
    _type = 'words'
    child_class = None

    @staticmethod
    def parse(text):
        return text.split(' ')