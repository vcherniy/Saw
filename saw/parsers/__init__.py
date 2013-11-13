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
                    result.append(old_items)
                    result.append(node)
                    old_items = []

            items = list(text[curr: _next])
            if (curr > 0) and (text[curr - 1] == ' '):
                items[0] = ' ' + items[0]
            if (_len > _next) and (text[_next] == ' '):
                items[-1] += ' '
            old_items.extend(items)

            prev = _next

        result.append(old_items)

        if _len > prev:
            node = text[prev:].strip()
            if node:
                result.append(node)
                result.append([])
        return result

    @classmethod
    def load(cls, saw: Item, text, process_modificators = True):
        saw.children = []
        need_new = True

        for item in cls.parse(text):
            if isinstance(item, list):
                # If it is no first item
                # (first item is empty, and words array has not nodes)
                if need_new and item:
                    saw.children.append(Item())
                    need_new = False
                for n in item:
                    # if ' x' and before it no string (were another nodes in list)
                    # because string join first node after it whether this node has left-space or not
                    if n[0] == ' ' and saw.children[-1].after_count():
                        saw.children.append(Item())
                        saw.children[-1].after_append(n.strip())
                    # if 'x ' then append node to current item and request
                    # create new item on next iteration.
                    elif n[-1] == ' ':
                        saw.children[-1].after_append(n.strip())
                        need_new = True
                    else:
                        if not cls._type == 'paragraphs':
                            n = n.strip()
                        saw.children[-1].after_append(n)
            else:
                saw.children.append(Item())
                # TODO: Fix it asap
                if cls._type == 'words':
                    saw.children[-1].text(item)
                # right nodes will be joined to it string
                need_new = False
        return saw
