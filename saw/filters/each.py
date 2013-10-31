class Each:
    def item(self, item):
        return self.items( item.children )

    def items(self, items):
        self.__items = [ item for item in items ]
        return self

    def get(self):
        return self.__items

    def __getattr__(self, name):
        if hasattr(self.__items[0], name):
            for key, item in enumerate(self.__items):
                self.__items[key] = getattr(item, name)

            if callable( self.__items[0] ):
                def wrapper(*args, **kw):
                    for key, item in enumerate(self.__items):
                        self.__items[key] = item(*args, **kw)
                    return self
                return wrapper
            return self
        raise AttributeError(name)