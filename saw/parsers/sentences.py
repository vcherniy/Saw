from saw.parsers.blocks import Parser, Blocks


class Sentences(Parser):
    _child_class = Blocks
    _delimiters = ['!', '?', '.']
