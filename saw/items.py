from filters import Filter


class Items(list):
    _str_dir = dir('')

    def __str__(self):
        return ' '.join((x.__str__() for x in self))

    def __getattr__(self, name):
        name = str(name)

        if name in self._str_dir:
            result = Items(getattr(item, name) for item in self)

            if result and callable(result[0]):
                def wrapper(*args, **kw):
                    return Items(func(*args, **kw) for func in result)
                return wrapper
            return result

        if Filter.exists(name):
            return Filter.get(name, self)

        result = Items()
        for item in self:
            result.extend(getattr(item, name, []))
        return result

    def __getitem__(self, key):
        result = super(Items, self).__getitem__(key)
        if isinstance(key, slice):
            result = Items(result)
        return result

    def __getslice__(self, i, j):
        result = super(Items, self).__getslice__(i, j)
        return Items(result)