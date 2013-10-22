class Item:
    # has attribute with direch children and name as children type
    # example: .words

    def init(self, after_arr):
        self.after(after_arr)

    def after(self, after_arr):
        self._after_arr = after_arr

    def text(self, text):
        self._text = text

    # has attribute .children with link to above attribute.

    # if we call instance with attribute what exists in instance then
    # python will take direct access to children.
    # else call this function
    def __getattr__(self, name):
        name = str(name)
        result = Items()

        if 'children' in self.__dict__:
            for item in self.children:
                result.extend( getattr(item, name, []) )
        return result

class Items(list, Item):
    def ii(self):
        print 'o'

    def __getitem__(self, key):
        return super(Items, self).__getitem__()

    def __iter__(self):
        return super(Items, self).__iter__()


    def next(self):
        return super(Items, self).next()


from parser import Parse

class Saw():
    def load(self, text):
        return Parse.load(text)
