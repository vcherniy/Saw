import base
from words import Words
import re


class Blocks(base.Base):
    _type = 'blocks'
    child_class = Words

    @staticmethod
    def parse(text):
        _len = len(text)
        result = []
        prev = 0

        # we allow .09 as not end of sentences
        for m in re.finditer('[\,\:\=\+\;\*\{\(\[\]\)\}\"\-' + "\\'" + ']+', text):
            curr, _next = m.start(), m.end()
            items = list( text[curr: _next].strip() )

            if (_len > _next) and not (text[_next] == ' '):
                # delete ending '.' if they not before space or end of string
                while (len(items) > 0) and (items[-1] in ['-', "'"]):
                    items.pop()
                    _next = _next - 1

            if len(items) > 0:
                # if prev position of delimiter < current - between exists text
                # at least 1 symbol.
                if prev < curr:
                    node = text[prev:curr].strip()
                    if node != '':
                        result.append(node)
                result.append( items )
                prev = _next
        if _len > prev:
            node = text[prev:].strip()
            if node:
                result.append(node)
        return result
