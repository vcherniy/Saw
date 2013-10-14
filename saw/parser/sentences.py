import base
from blocks import Blocks
import re

class Sentences(base.Base):
    _type = 'sentences'
    child_class = Blocks

    @staticmethod
    def parse(text):
        #re.split('\!|\?|\. | \.',text)
        result = []
        prev = 0

        # we allow .09 as not end of sentences
        #for m in re.finditer('[\!\?]+|\.+(?:\s+|$|\?|\!)', text):
        for m in re.finditer('\.+(?:\s+|$)|(\.*)[\!\?]+(\.+(?:\s+|$))*', text):
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