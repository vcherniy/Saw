from saw.node import Node


class Filter:
    def __init__(self):
        pass

    @staticmethod
    def filter(node, func):
        result = Node()
        for item in node:
            if func(item):
                result.append(item)
        return result.type(node.type())