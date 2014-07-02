class Pure:
    def __init__(self):
        pass

    @staticmethod
    def filter(node):
        new_node = node.copy(lambda x: x.pure())
        return new_node.before([]).after([])