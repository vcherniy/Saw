class Sentences(Saw_Base):
    _type = 'sentences'
    child_class = Saw_Blocks

    @staticmethod
    def parse(text):
        # x.extend(
        return text.split('.')