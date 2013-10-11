class Blocks(Base):
    _type = 'blocks'
    child_class = Saw_Words

    @staticmethod
    def parse(text):
        return text.split(',')