from saw.parsers.blocks import Parser, Blocks


class Sentences(Parser):
    _type = 'sentences'
    _child_class = Blocks
    _format = '[!\?\.]+'