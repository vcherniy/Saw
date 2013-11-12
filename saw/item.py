from saw.items import Items
from saw.filters import Filter

class Item:
    # has attribute with direch children and name as children type
    # example: .words
    _str_dir = dir('')

    def __init__(self):
        self._after = []
        self._text = ''
        self.children = None

    def after(self, _after):
        self._after = _after

    def text(self, text):
        self._text = text

    def __repr__(self):
        result = self.__dict__
        result.pop("children", None)
        if not(self._after): result.pop('_after', None)
        if not(self._text):  result.pop('_text', None)
        return result.__repr__()

    def __str__(self):
        return "%s%s%s" % (str(self.children or ''), self._text, ''.join(self._after))

    # if we call instance with attribute what exists in instance then
    # python will take direct access to children.
    # else call this function
    def __getattr__(self, name):
        name = str(name)

        if name in self._str_dir:
            return getattr(self.__str__(), name)

        if Filter.exists(name):
            return Filter.get(name, self)

        result = Items()
        if ('children' in self.__dict__) and self.children:
            result = getattr(self.children, name, [])
        return result