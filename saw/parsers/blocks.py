from saw.parsers.words import Parser, Words


class Blocks(Parser):
    _child_class = Words
    _delimiters = [',', ':', '=', '+', ';', '*', '"', '-', "'", '{', '(', '[', ']', ')', '}']
