from saw.node import Node


class Each:
    def __init__(self):
        self.__node = []

    def filter(self, node):
        self.__node = node
        return self

    def get(self, to_node=True):
        if to_node:
            self.__node = Node(x for x in self.__node)
        return self.__node

    def __getattr__(self, attr):
        if self.__node:
            self.__node = [getattr(item, attr) for item in self.__node]

            if callable(self.__node[0]):
                def wrapper(*args, **kw):
                    self.__node = [func(*args, **kw) for func in self.__node]
                    return self
                return wrapper
        return self