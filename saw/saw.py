class Item:
    # has attribute with direch children and name as children type
    # example: .words

    def __init__(self, klass):
        self._live = False
        self.__klass = klass.child_class

    def after(self, after_arr):
        self.live()
        self._after_arr = after_arr

    def text(self, text):
        self.live()
        self._text = text

    def live(self):
        self._live = True

    def __repr__(self):
        if self.__klass:
            return self.__klass.repr(self)
        elif '_text' in self.__dict__:
            return self._text
        else:
            return ''



    # has attribute .children with link to above attribute.



    # if we call instance with attribute what exists in instance then
    # python will take direct access to children.
    # else call this function
    def __getattr__(self, name, *args, **kwrds):
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
