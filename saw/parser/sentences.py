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
        tmp = []

        for m in re.finditer('\!|\?| \.|\.(?:\s+|$)', text):
            curr = m.start()
            if prev < curr:
                if tmp:
                    result.append(tmp)
                    tmp = []
                result.append(text[prev:curr].strip())
            tmp.append(text[curr])
            prev = curr + 1
        result.append(tmp)
        if len(text) > prev:
            result.append(text[prev:].strip())
        return result