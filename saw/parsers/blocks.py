from saw.parsers.words import Parser, Words


class Blocks(Parser):
    _type = 'blocks'
    _child_class = Words
    _format = '[\,\:\=\+\;\*\{\(\[\]\)\}\"\-' + "\\'" + ']+'
