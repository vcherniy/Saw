class Item:
    # has attribute with direch children and name as children type
    # example: .words

    def __init__(self):
        self._live = False

    def after(self, after_arr):
        self.live()
        self._after_arr = after_arr

    def text(self, text):
        self.live()
        self._text = text

    def live(self):
        self._live = True

    # has attribute .children with link to above attribute.

    def __repr__(self):
        #return super(Items, self).__repr__()
        return list.__repr__(self)

    # if we call instance with attribute what exists in instance then
    # python will take direct access to children.
    # else call this function
    def __getattr__(self, name, *args, **kwrds):
        print 'GET ' + str(self.__dict__.keys()) + ':: ' + name

        if name in list.__dict__:
            def fn(*args, **kwrds):
                return getattr(list, name)(*args, **kwrds)
            return fn

        name = str(name)
        result = Items()

        if 'children' in self.__dict__:
            for item in self.children:
                result.extend( getattr(item, name, []) )
            return result
        return list()

class Items(list, Item):
    def ii(self):
        print 'o'


from parser import Parse

class Saw():
    def load(self, text):
        return Parse.load(text)
