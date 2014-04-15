class Pure:
    @staticmethod
    def filter(node):
        new_node = node.__class__(x.pure() for x in node)
        new_node.__dict__ = node.__dict__.copy()
        new_node.before([]).after([])
        return new_node