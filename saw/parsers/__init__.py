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

    # =========== Load ==============

    @classmethod
    def _process_mods(cls, data):
        Mod.load_mods()
        for i in range(0, len(data) - 1, 2):
            tmp = Mod.get(cls._type, data[i: i + 3])
            data[i], data[i+1], data[i+2] = tmp[0], tmp[1], tmp[2]
        return data

    @classmethod
    def _process_string(cls, saw, text):
        saw.children.append(Item())

    @classmethod
    def _process_list(cls, saw, item):
        if not item:
            return

        # delete first space into first list item
        # prevent add new item right after text string
        if item[0][0] == ' ':
            item[0] = item[0][1:]

        need_new = False
        for n in item:
            # if ' x' and before it no string (were another nodes in list)
            # because string join first node after it whether this node has left-space or not
            if n[0] == ' ':
                saw.children.append(Item())
                saw.children[-1].after_append(n.strip())
                need_new = False
            # if 'x ' then append node to current item and request
            # create new item on next iteration.
            else:
                # If it is no first item
                # (first item is empty), (words has not nodes)
                if need_new:
                    saw.children.append(Item())
                    need_new = False
                if n[-1] == ' ':
                    saw.children[-1].after_append(n.strip())
                    need_new = True
                else:
                    # TODO: fix it asap
                    if not cls._type == 'paragraphs':
                        n = n.strip()
                    saw.children[-1].after_append(n)

    @classmethod
    def _load(cls, saw, data):
        if data[0]:
            saw.children.append(Item())

        cls._process_list(saw, data[0])
        for i in range(1, len(data) - 1, 2):
            cls._process_string(saw, data[i])
            cls._process_list(saw, data[i + 1])

    @classmethod
    def load(cls, saw: Item, text, process_mods=True):
        saw.children = []
        data = cls.parse(text)
        if process_mods:
            data = cls._process_mods(data)

        cls._load(saw, data)
        return saw

