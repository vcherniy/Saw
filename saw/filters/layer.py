class Layer:
    @staticmethod
    def filter(node, name, layer_func):
        for k in node:
            k.type(name)
            layer_func(k)