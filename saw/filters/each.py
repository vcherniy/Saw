class Each:
    def __init__(self):
        self.__items = []

    def item(self, item):
        return self.items(item.children)

    def items(self, items):
        self.__items = [item for item in items]
        return self

    def get(self, level=1):
        level -= 1
        if level > 0:
            return self.__getattr__('get')(level)
        else:
            return self.__items

    def __getattr__(self, attr):
        if self.__items:
            self.__items = [getattr(item, attr) for item in self.__items]

            if callable(self.__items[0]):
                def wrapper(*args, **kw):
                    self.__items = [func(*args, **kw) for func in self.__items]
                    return self
                return wrapper
        return self