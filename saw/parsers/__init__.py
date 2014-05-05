from saw.node import Node
import re
from saw.mods import Mod


class Parser:
    _type = ''
    _format = ''
    _child_class = None

    enable_process_mods = True

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

    @classmethod
    def process_mods(cls, data):
        Mod.init()
        result = []

        if data:
            last_node = data[0]
            for i in xrange(0, len(data) - 2, 2):
                tmp = Mod.get(cls._type, last_node, data[i+1], data[i+2], i == 0)
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

    # =========== Load ==============

    @classmethod
    def _append(cls, saw, text=''):
        if text:
            if cls._child_class:
                node = cls._child_class.load(text)
            else:
                node = Node().text(text)
        else:
            node = Node()
            if cls._child_class:
                node.type(cls._child_class._type)
        saw.append(node)
        return saw[-1]

    @classmethod
    def _process_list(cls, saw, arr):
        if not arr:
            return []

        #  . , |.,|
        to_before = []
        while arr and (len(arr[-1]) == 1):
            to_before.insert(0, arr.pop())

        if arr:
            # add to to_before element ' |<any count spaces>.|..text'
            if not arr[-1][-1] == ' ':
                to_before.insert(0, arr.pop().strip())

            # still items just for _after -- 'x..y' and 'x ..y' items were excluded
            if arr:
                # first item should be attached to current last text item
                if arr[0][0] == ' ':
                    arr[0] = arr[0][1:]
                # if Node empty then append item to him
                # because we should set _after for last item of Node
                need_new = not saw

                for item in arr:
                    if item == ' ':
                        need_new = True
                    to_before_mode = (item[:2] == '  ')
                    if need_new:
                        cls._append(saw)
                        need_new = False
                    if item[-1] == ' ':
                        need_new = True
                    if to_before_mode:
                        saw[-1].before(item.strip(), True)
                    else:
                        saw[-1].after(item.strip(), True)
        # there was 'x..y', because we must set ['.', '.'] as _after of last item of Node
        # if Node is empty then there was begin of string then leave _before for next Node's item
        elif saw:
            saw[-1].after(to_before)
            to_before = []
        return to_before

    @classmethod
    def _load_children(cls, saw, data):
        # to_before - node items for _before of current string item
        # process first item - always '[...]'
        to_before = cls._process_list(saw, data[0])
        # each pair: text, [...]
        for i in xrange(1, len(data) - 1, 2):
            cls._append(saw, data[i]).before(to_before)
            to_before = cls._process_list(saw, data[i + 1])
        if to_before:
            cls._append(saw).after(to_before)

    @classmethod
    def load(cls, text):
        saw = Node().type(cls._type)

        data = cls.parse(text)
        if cls.enable_process_mods:
            data = cls.process_mods(data)
        cls._load_children(saw, data)
        return saw