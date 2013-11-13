from saw.items import Items
from saw.item import Item
import re


class Parser:
    _type = ''
    _format = ''
    _child_class = None

    @classmethod
    def parse(cls, text):
        _len = len(text)
        result = []
        prev = 0
        old_items = []

        for m in re.finditer(cls._format, text):
            curr, _next = m.start(), m.end()

            if prev < curr:
                node = text[prev:curr].strip()
                if node != '':
                    if old_items:
                        result.append(old_items)
                        old_items = []
                    result.append(node)

            items = list(text[curr: _next])
            if (curr > 0) and (text[curr - 1] == ' '):
                items[0] = ' ' + items[0]
            if (_len > _next) and (text[_next] == ' '):
                items[-1] += ' '
            old_items.extend(items)

            prev = _next

        if old_items:
            result.append(old_items)

        if _len > prev:
            node = text[prev:].strip()
            if node:
                result.append(node)
        return result

    @classmethod
    def load(cls, saw, text):
        children, item = Items(), Item()

        for item_text in cls.parse(text):
            if isinstance(item_text, list):
                item.after(item_text)
            elif cls._child_class:
                cls._child_class.load(item, item_text)
                continue
            else:
                item.text(item_text)

            children.append(item)
            item = Item()
        # When ._text or ._after were assigned, it items were
        # added to children
        if item.children:
            children.append(item)
        if children:
            saw.__dict__[cls._type] = saw.children = children