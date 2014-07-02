class Layer:
    def __init__(self):
        pass

    @staticmethod
    def filter(node, name, layer_func):
        for k in node:
            k.type(name)
            layer_func(k)