from filters import Filter


class Node(list):
    # get attributes of String class
    _str_dir = dir('')

    def __init__(self, *args, **kwrd):
        self._before, self._after = [], []
        self._text, self._type = '', ''
        super(Node, self).__init__(*args, **kwrd)

    def type(self, _type):
        self._type = _type
        return self

    def before(self, value, _append=False):
        if _append:
            self._before.append(value)
        else:
            self._before = value
        return self

    def after(self, value, _append=False):
        if _append:
            self._after.append(value)
        else:
            self._after = value
        return self

    def text(self, text, _append=False):
        if _append:
            self._text += text
        else:
            self._text = text
        return self

    #def __repr__(self):
    #    return dict((x, y) for x, y in self.__dict__.copy().iteritems()
    #                if y and not (x == 'children')).__repr__()

    def __str__(self):
        children_text = ' '.join((str(x) for x in self))
        return ''.join([''.join(self._before), children_text, self._text, ''.join(self._after)])

    # if we call instance with attribute what exists in instance then
    # python will take direct access to children.
    # else call this function
    def __getattr__(self, name):
        name = str(name)

        if name in self._str_dir:
            # get str hash of this object and apply attribute to this
            return getattr(str(self), name)

        #if name in self._str_dir:
        #    result = Items(getattr(item, name) for item in self)

        #    if result and callable(result[0]):
        #        def wrapper(*args, **kw):
        #            return Items(func(*args, **kw) for func in result)
        #        return wrapper
        #    return result

        if Filter.exists(name):
            return Filter.get(name, self)

        result = Node()
        if not self:
            for item in self:
                result.extend(getattr(item, name))
        return result

    def __getitem__(self, key):
        result = super(Node, self).__getitem__(key)
        if isinstance(key, slice):
            result = Node(result).type(self._type)
        return result

    def __getslice__(self, i, j):
        result = super(Node, self).__getslice__(i, j)
        return Node(result).type(self._type)