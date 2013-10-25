
class Item:
    # has attribute with direch children and name as children type
    # example: .words

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

    @property
    def pure(self):
        item = Item()
        item.__dict__ = self.__dict__.copy()
        item.__dict__.pop('_after', None)
        return item

    # if we call instance with attribute what exists in instance then
    # python will take direct access to children.
    # else call this function
    def __getattr__(self, name):
        name = str(name)
        result = Items()

        if self.children:
            result = getattr(self.children, name, [])
        return result

    def __getitem__(self, key):
        return self.__str__().__getitem__(key)

    def __getslice__(self, i, j):
        return self.__str__().__getslice__(i, j)


class Items(list):
    def __str__(self):
        return ' '.join( (str(x) for x in self) )

    def __getattr__(self, name):
        name = str(name)
        result = Items()

        for item in self:
            result.extend( getattr(item, name, []) )
        return result

    @property
    def pure(self):
        return Items( x.pure for x in self )

    def __getitem__(self, key):
        result = super(Items, self).__getitem__(key)
        if isinstance(key, slice):
            result = Items(result)
        return result

    def __getslice__(self, i, j):
        result = super(Items, self).__getslice__(i, j)
        return Items(result)        


from parser import Parse

class Saw():
    def load(self, text):
        return Parse.load(text)