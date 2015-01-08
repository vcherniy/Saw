"""
@TODO
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

def add_triad(layer):
    text = layer.get_node().text()
    for i in xrange(0, len(text) - 2):
        triad = Node().text(text[i: i + 3])
        layer.append(triad)

sw.words.layer('triads', add_triad)
for tr in sw.triads:
    print tr

print '---- filter ----'
for tr in sw.triads.filter(lambda x: 'f' in x.text().lower()):
    print tr
"""