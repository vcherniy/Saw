class Layer:
    def __init__(self):
        self._node = None

    def filter(self, node, name, layer_func):
        for item in node:
            self._node = item.type(name)
            layer_func(self)
            self._node.text('')
        return node

    def get_node(self):
        return self._node

    def append(self, item):
        self._node.append(item)