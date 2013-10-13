import base
from words import Words
import re

class Blocks(base.Base):
    _type = 'blocks'
    child_class = Words

    @staticmethod
    def parse(text):
        result = []
        prev = 0

        # we allow "-cast" and "'case" as not end of block
        # commented: | \-| \'
        #for m in re.finditer('[\!\?]+|\.+(?:\s+|$)', text):
        for m in re.finditer('[\,\:\=\+\;\*\{\(\[\]\)\}\"]+|[\-\']+(?:\s+|$)', text):
            curr, _next = m.start(), m.end()
            # if prev position of delimiter < current - between exists text
            # at least 1 symbol.
            if prev < curr:
                node = text[prev:curr].strip()
                if node != '':
                    result.append(node)
            result.append(list( text[curr:_next].strip() ))
            prev = _next
        if len(text) > prev:
            result.append(text[prev:].strip())
        return result