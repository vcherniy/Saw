from saw.items import Items
from saw.item import Item
import re
from saw.mods import Mod


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

            # append string and nodes what were before it
            if prev < curr:
                node = text[prev:curr].strip()
                if node != '':
                    result.append(old_items)
                    result.append(node)
                    old_items = []
            # format nodes
            items = list(text[curr: _next])
            if (curr > 0) and (text[curr - 1] == ' '):
                items[0] = ' ' + items[0]
            if (_len > _next) and (text[_next] == ' '):
                items[-1] += ' '
            old_items.extend(items)
            # set start for next iteration
            prev = _next

        # Whether empty or not - last item must be List.
        result.append(old_items)
        # If after last nodes exists string
        if _len > prev:
            node = text[prev:].strip()
            if node:
                result.append(node)
                result.append([])
        return result

    @classmethod
    def load(cls, saw: Item, text, process_mods=True):
        saw.children = []
        data = cls.parse(text)

        if process_mods:
            # TODO: fix asap
            if cls._type != 'words':
                Mod.load_mods()
                for i in range(0, len(data) - 1, 2):
                    tmp = Mod.get(cls._type, data[i: i + 3])
                    data[i], data[i+1], data[i+2] = tmp[0], tmp[1], tmp[2]
                data = [item for item in data if item]

        prev_type = 'list'
        need_new = True

        for item in data:
            if isinstance(item, list):
                prev_type = 'list'
                # If it is no first item
                # (first item is empty), (words has not nodes)
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
                if prev_type != 'str':
                    saw.children.append(Item())
                # TODO: Fix it asap
                if cls._type == 'words':
                    saw.children[-1].text_append(item)
                # right nodes will be joined to it string
                need_new = False
                prev_type = 'str'
        return saw
