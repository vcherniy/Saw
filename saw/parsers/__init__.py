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
        while arr and arr[-1].none():
            to_before.insert(0, arr.pop().symbol)

        if arr:
            # add to to_before element ' | .|..text'
            if arr[-1].left():
                to_before.insert(0, arr.pop().symbol)

            # still items just for _after -- 'x..y' and 'x ..y' items were excluded 
            i, cnt = 0, len(arr)
            if arr:
                # first item should be attached to current last text item
                arr[0].left(False)
                # if last text item not exists then create him 
                # because _after should be added to it
                if not saw.children:
                    saw.children.append(Item())
            # attached 'x..' to last text item
            while (i < cnt) and arr[i].none():
                saw.children[-1].after_append(arr[i].symbol)
                i += 1

            # attached 'x..|.| ' to last text item too
            if (i < cnt) and arr[i].right():
                saw.children[-1].after_append(arr[i].symbol)
                i += 1

            if i < cnt:
                need_new = True
                while i < cnt:
                    if arr[i].left() or arr[i].both():
                        need_new = True
                    if need_new:
                        saw.children.append(Item())
                        need_new = False
                    if arr[i].right() or arr[i].both():
                        need_new = True
                    saw.children[-1].after_append(arr[i].symbol)
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
        cls._convert(data)
        if process_mods:
            data = cls._process_mods(data)
        cls._load_children(saw, data)

        if cls._child_class:
            for x in saw.children:
                cls._child_class.load(x, x._text, process_mods)
                x._text = ''
        return saw

    @staticmethod
    def _convert(data):
        for i in xrange(0, len(data), 2):
            for j in xrange(0, len(data[i])):
                data[i][j] = Node(data[i][j])

class Node:
    _left = False
    _right = False
    include_to = False
    symbol = ''

    def __init__(self, source):
        if source[0] == ' ':
            self._left = True
        if source[-1] == ' ':
            self._right = True
        self.symbol = source
        if self._left or self._right:
            self.symbol = source.strip()

    def left(self, status = None):
        if status == None:
            return self._left and not self._right
        elif status in [False, True]:
            self._left = status
            if status:
                self._right = False
            return self

    def right(self, status = None):
        if status == None:
            return self._right and not self._left
        elif status in [False, True]:
            self._right = status
            if status:
                self._left = False
            return self

    def both(self, status = None):
        if status == None:
            return self._left and self._right
        elif status in [False, True]:
            self._right = status
            self._left = status
            return self

    def none(self):
        return not(self._left or self._right)

    def __repr__(self):
        return repr([self._left, self.symbol, self._right])