class Paragraphs(Saw_Base):
    _type = 'paragraphs'
    child_class = Saw_Sentences

    @staticmethod
    def parse(text):
        return [text]