from items import Items
from filters import Filter


class Item:
    # get attributes of String class
    _str_dir = dir('')

    def __init__(self):
        self._before = []
        self._after = []
        self._text = ''
        self.children = None

    def set_children_alias(self, name):
        setattr(self, name, self.children)

    def before(self, _before):
        self._before = _before
        return self

    def before_append(self, item):
        self._before.append(item)
        return self

    def after(self, _after):
        self._after = _after
        return self

    def after_append(self, item):
        self._after.append(item)
        return self

    def text(self, text):
        self._text = text
        return self

    def text_append(self, text):
        self._text += text
        return self

    def __repr__(self):
        return dict((x, y) for x, y in self.__dict__.copy().iteritems()
                    if y and not (x == 'children')).__repr__()

    def __str__(self):
        return "%s%s%s%s" % (''.join(self._before), str(self.children or ''), self._text, ''.join(self._after))

    # if we call instance with attribute what exists in instance then
    # python will take direct access to children.
    # else call this function
    def __getattr__(self, name):
        name = str(name)

        if name in self._str_dir:
            # get str hash of this object and apply attribute to this
            return getattr(self.__str__(), name)

        if Filter.exists(name):
            return Filter.get(name, self)

        result = Items()
        if self.children:
            result = getattr(self.children, name)
        return result