class Lower:
    def __init__(self):
        pass

    @staticmethod
    def filter(node):
        new_node = node.copy(lambda x: x.lower())
        return new_node.text(node.text().lower())