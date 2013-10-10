class Saw_Items(list):
    def __getattr__(self, name):
        name = str(name)

        for _type in self.__dict__:
            result = Saw_Items()
            for item in self.__dict__[_type]:
                result.extend( getattr(item, name, []) )

            if result:
                return result


class Saw():
    def load(self, text):
        saw = Saw_Items()
        Saw_Paragraphs.load(saw, text)
        return saw


class Saw_Base:
    @classmethod
    def load(self, saw, text):
        if not (self._type in saw.__dict__):
            saw.__dict__[ self._type ] = Saw_Items()

        items = self.parse(text)
        for item in items:
            if item == '':
                continue
            if self.child_class:
                item = self.child_class.load( Saw_Items(), item)
            saw.__dict__[ self._type ].append(item)
        return saw


class Saw_Words(Saw_Base):
    _type = 'words'
    child_class = None

    @staticmethod
    def parse(text):
        return text.split(' ')


class Saw_Blocks(Saw_Base):
    _type = 'blocks'
    child_class = Saw_Words

    @staticmethod
    def parse(text):
        return text.split(',')


class Saw_Sentences(Saw_Base):
    _type = 'sentences'
    child_class = Saw_Blocks

    @staticmethod
    def parse(text):
        # x.extend(
        return text.split('.')


class Saw_Paragraphs(Saw_Base):
    _type = 'paragraphs'
    child_class = Saw_Sentences

    @staticmethod
    def parse(text):
        return [text]


text = "Starting right this second, it's way easier to merge Pull Requests! We usually merge them from the comfortable glow of our computers, but with the new mobile site we're comfortable merging smaller Pull Requests while sitting on the hyperloop (or while on the bus, I guess)."
parse = Saw().load(text)
for bl in parse.paragraphs[0].sentences[0].blocks:
    print bl.words[:2]

print "---------- \n"
for bl in parse.blocks:
    print bl.words[:2]

