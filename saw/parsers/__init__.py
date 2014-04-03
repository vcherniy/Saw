#from saw.items import Items
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
        Mod.init()

        for i in xrange(0, len(data) - 2, 2):
            # pass [[,,], 'text', [,,]]
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
    def _process_list(cls, saw, arr):
        if not arr:
            return []

        #  . , |.,|
        to_before = []
        while arr and (len(arr[-1]) == 1):
            to_before.insert(0, arr.pop())

        if arr:
            _ln_last = len(arr[-1])
            # add to to_before element ' | .|..text'
            if _ln_last == 2 and arr[-1][0] == ' ':
                to_before.insert(0, arr.pop().strip())

            # add to to_before element ' |  .|..text'
            if _ln_last == 3 and arr[-1][:2] == '  ':
                to_before.insert(0, arr.pop().strip())

            # still items just for _after -- 'x..y' and 'x ..y' items were excluded 
            i, cnt = 0, len(arr)
            if cnt > 0:
                # first item should be attached to current last text item
                if arr[0][0] == ' ':
                    arr[0] = arr[0][1:]
                # if last text item not exists then create him 
                # because _after should be added to it
                need_new = False
                to_before_mode = False
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
        # if children then were 'x..y' and add '..' to 'x' as after 
        # else add to _before next text item - y (just <begin string>'..y') 
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
        saw.children = []

        data = cls.parse(text)
        if process_mods:
            data = cls._process_mods(data)
        cls._load_children(saw, data)

        if cls._child_class:
            for x in saw.children:
                cls._child_class.load(x, x._text, process_mods)
                x._text = ''
        return saw

    @staticmethod
    def to_before(item):
        return getattr(item, 'to_before', False) == True

    @staticmethod
    def to_after(item):
        return getattr(item, 'to_after', False) == True