
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
        return "%s%s%s" % (str(self.children or ''), self._text, ''.join(self._after))

    def __str__(self):
        return self.__repr__()

    # if we call instance with attribute what exists in instance then
    # python will take direct access to children.
    # else call this function
    def __getattr__(self, name):
        name = str(name)
        result = Items()

        if self.children:
            result = getattr(self.children, name, [])
        return result


class Items(list):
    def __repr__(self):
        return ' '.join( (str(x) for x in self) )

    def __getattr__(self, name):
        name = str(name)
        result = Items()

        for item in self:
            result.extend( getattr(item, name, []) )
        return result

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