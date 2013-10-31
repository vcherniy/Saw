class Each:
    def item(self, item):
        return self.items( item.children )

    def items(self, items):
        self.__items = [ item for item in items ]
        return self

    def get(self):
        return self.__items

    def __getattr__(self, name):
        if len(self.__items):
            self.__items = [ getattr(item, name) for item in self.__items ]

            if callable( self.__items[0] ):
                def wrapper(*args, **kw):
                    self.__items = [ item(*args, **kw) for item in self.__items ]
                    return self
                return wrapper
        return self