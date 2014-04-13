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
                if node:
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
        Mod.init()

        if data:
            result = []
            last_node = data[0]

            for i in xrange(0, len(data) - 2, 2):
                tmp = Mod.get(cls._type, last_node, data[i+1], data[i+2])
                # if _before is empty then append _text to last result node - always text node.
                # if result is empty then leave as is and append to result
                if not tmp[0] and result:
                    result[-1] += tmp[1]
                else:
                    result.append(tmp[0])
                    result.append(tmp[1])
                last_node = tmp[2]
            result.append(last_node)
        return result

    @classmethod
    def _process_string(cls, saw, text, to_before):
        saw.children.append(Item().before(to_before).text(text))

    @classmethod
    def _process_list(cls, saw, arr):
        if not arr:
            return []

        #  . , |.,|
        to_before = []
        while arr and (len(arr[-1]) == 1):
            to_before.insert(0, arr.pop())

        if arr:
            # add to to_before element ' | .|..text' and ' |  .|..text'
            if not arr[-1][-1] == ' ':
                to_before.insert(0, arr.pop().strip())

            # still items just for _after -- 'x..y' and 'x ..y' items were excluded 
            i, cnt = 0, len(arr)
            if cnt > 0:
                # first item should be attached to current last text item
                if arr[0][0] == ' ':
                    arr[0] = arr[0][1:]
                need_new = False
                to_before_mode = False
                # if last text item not exists then create him
                # because _after should be added to it
                if not saw.children:
                    need_new = True

                while i < cnt:
                    if arr[i][0] == ' ':
                        need_new = True
                    to_before_mode = (arr[i][:2] == '  ')
                    if need_new:
                        saw.children.append(Item())
                        need_new = False
                    if arr[i][-1] == ' ':
                        need_new = True
                    if to_before_mode:
                        saw.children[-1].before_append(arr[i].strip())
                    else:
                        saw.children[-1].after_append(arr[i].strip())
                    i += 1
        # if children then were 'x..y' then should add '..' to 'x' as after
        # else if begin of string then children is empty and add '..' to _before
        elif saw.children:
            saw.children[-1].after(to_before)
            to_before = []
        return to_before

    @classmethod
    def _load_children(cls, saw, data):
        # to_before - node items for _before of current string item
        # process first item - always '[...]'
        to_before = cls._process_list(saw, data[0])
        # each pair: text, [...]
        for i in xrange(1, len(data) - 1, 2):
            cls._process_string(saw, data[i], to_before)
            to_before = cls._process_list(saw, data[i + 1])
        if to_before:
            saw.children.append(Item().after(to_before))

    @classmethod
    def load(cls, saw, text, process_mods=True):
        saw.children = Items()

        data = cls.parse(text)
        if process_mods:
            data = cls._process_mods(data)
        cls._load_children(saw, data)

        if cls._child_class:
            for child in saw.children:
                cls._child_class.load(child, child._text, process_mods)
                child._text = ''
        saw.set_children_alias(cls._type)
        return saw