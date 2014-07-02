class Call:
    def __init__(self):
        pass

    @staticmethod
    def filter(node, func):
        return node.copy(func)