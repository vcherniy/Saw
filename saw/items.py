from filters import Filter

class Items(list):
    def __str__(self):
        return ' '.join( (str(x) for x in self) )

    def __getattr__(self, name):
        name = str(name)
        result = Items()

        if Filter.exists(name):
            return Filter.get(name, self)

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