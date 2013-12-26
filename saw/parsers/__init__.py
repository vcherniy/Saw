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
            data[i], data[i + 1], data[i + 2] = tmp[0], tmp[1], tmp[2]

        # correct string if list is empty
        _max = len(data) - 3
        _from, _to = 2, 1
        while _from <= _max:
            if not data[_from]:
                data[_to] += data[_from + 1]
                data[_from + 1] = ''
            else:
                _to = _from + 1
            _from += 2
        return data

    @classmethod
    def _process_string(cls, saw, text, to_before):
        if not text:
            return
        saw.children.append(Item().before(to_before).text(text))

    @classmethod
    def _process_list(cls, saw, item):
        if not item:
            return []

        to_before = []
        while item and (len(item[-1]) == 1):
            to_before.append(item.pop())

        if item:
            # add to to_before element ' | .|..text'
            if item[-1][0] == ' ' and (len(item[-1]) == 2):
                to_before.append(item.pop().strip())

            i, cnt = 0, len(item)
            if item:
                item[0] = item[0].strip()
                if not saw.children:
                    saw.children.append(Item())
            while (i < cnt) and (len(item[i]) == 1):
                saw.children[-1].after_append(item[i])
                i += 1

            if (i < cnt) and (item[i][1] == ' '):
                saw.children[-1].after_append(item[i].strip())
                i += 1

            if i < cnt:
                need_new = True
                while i < cnt:
                    if item[i][0] == ' ':
                        need_new = True
                    if need_new:
                        saw.children.append(Item())
                        need_new = False
                    if item[i][-1] == ' ':
                        need_new = True
                    saw.children[-1].after_append(item[i].strip())
                    i += 1
        elif saw.children:
            saw.children[-1].after(to_before)
            to_before = []
        return to_before

    @classmethod
    def _load_children(cls, saw, data):
        to_before = cls._process_list(saw, data[0])
        for i in range(1, len(data) - 1, 2):
            cls._process_string(saw, data[i], to_before)
            to_before = cls._process_list(saw, data[i + 1])
        if to_before:
            saw.children.append(Item().after(to_before))

    @classmethod
    def load(cls, saw: Item, text, process_mods=True):
        saw.children = []
        #Mod.load_mods()

        data = cls.parse(text)

        if process_mods:
            data = cls._process_mods(data)

        cls._load_children(saw, data)

        """ For filters after
        if process_mods:
            ln = len(saw.children)
            if ln == 1:
                Mod.get(cls._type, Item(), saw.children[0], Item())
            elif ln == 2:
                Mod.get(cls._type, Item(), saw.children[0], saw.children[1])
            if ln > 2:
                for i in range(1, ln - 1):
                    Mod.get(cls._type, saw.children[i - 1], saw.children[i], saw.children[i + 1])
                Mod.get(cls._type, saw.children[-2], saw.children[-1], Item())
        """

        if cls._child_class:
            for x in saw.children:
                cls._child_class.load(x, x._text, process_mods)
                x._text = ''
        return saw