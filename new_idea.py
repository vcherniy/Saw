import re


class Iterator:
    def __iter__(self):
        self._iterator = 0
        self._nodes_len = len(self._nodes)
        return self

    def next(self):
        if self._nodes_len > self._iterator:
            result = self._nodes[self._iterator]
            self._iterator += 1
            return result
        else:
            raise StopIteration


class Layer(object, Iterator):
    format = None
    _base_layers = []

    def __init__(self, parent):
        self._nodes = []
        self._layers = {}
        self._parent_layer = parent
        self.text_obj = parent.text_obj
        # init nodes and layers
        self._init_nodes()
        self._init_layers()

    def _init_nodes(self):
        curr = None
        for re_node in re.finditer(self.__class__.format, self.text_obj.text):
            curr = self._add_node(curr, re_node.start(), re_node.end())
        # curr.end is end position of a last node
        if self.text_obj.text_len - 1 > curr.end:
            self._add_node(curr, self.text_obj.text_len, self.text_obj.text_len)

    def _add_node(self, curr, start, end):
        curr = Node(self.text_obj, curr, start, end - 1)
        self._nodes.append(curr)
        return curr

    def _init_layers(self):
        for layer in self.__class__._base_layers:
            self._layers[layer.__name__.lower()] = layer(self)

    def find_layer(self, find_name):
        if find_name in self._layers:
            return self._layers[find_name]
        else:
            for layer_name in self._layers:
                result = self._layers[layer_name].find_layer(find_name)
                if result:
                    return result
        return None

    @classmethod
    def _check_layer(cls, layer):
        return (layer is not None) and issubclass(layer, Layer)

    @classmethod
    def add_layer(cls, layer):
        if cls._check_layer(layer):
            cls._base_layers.append(layer)

    @classmethod
    def set_layer(cls, layer):
        if cls._check_layer(layer):
            for child in cls._base_layers:
                layer.add_layer(child)
            cls._base_layers = []
            cls.add_layer(layer)

    def __getattr__(self, name):
        name = str(name)
        return self.find_layer(name)


class Text(Layer):
    _base_layers = []

    def __init__(self, _text):
        self.text = _text
        self.text_len = len(_text)
        self.text_obj = self
        super(Text, self).__init__(self)
        # clear parent layer otherwise we will get endless parents
        self._parent_layer = None

    def _init_nodes(self):
        pass


class Sentences(Layer):
    format = '[\.\?!]+'
    _base_layers = []


class Blocks(Layer):
    format = '[\:\-\,]+'
    _base_layers = []


Text.add_layer(Sentences)
Sentences.add_layer(Blocks)


class Node:
    """
    Object's variables:
    .start - start position of the node
    .start_text - start position of node's symbols
    .end_text - end position of node's symbols
    .start_tokens - start position of tokens (symbols that explode text to nodes)
    .end - end position of the node

    ._layer - reference to the parent layer
    ._prev_node - reference to the prev node (or Null)
    ._next_node - reference to the next node (or Null)
    """
    def __init__(self, layer, prev_node, re_start, re_end):
        self._layer = layer
        # start node | # start text | # end text (include pos) | # start tokens | #end node (include pos)
        if prev_node:
            self.start = prev_node.end + 1
        else:
            self.start = 0
        self.start_tokens = re_start
        self.end = re_end
        # calculate start_string
        self.start_text = self.start
        while self.start_text < self.start_tokens and self._layer.text_obj.text[self.start_text] == ' ':
            self.start_text += 1
        # calculate end_string
        self.end_text = self.start_tokens - 1
        while self.end_text > self.start_text and self._layer.text_obj.text[self.end_text] == ' ':
            self.end_text -= 1
        # set links
        self._prev_node = prev_node
        self._next_node = None
        if prev_node:
            prev_node.next_node(self)

    def _get_by_pos(self, start, end):
        return self._layer.text_obj.text[start: end + 1]

    def text(self):
        return self._get_by_pos(self.start_text, self.end_text)

    def original(self):
        return self._get_by_pos(self.start, self.end)

    def __str__(self):
        return self.text()

    def next_node(self, node=None):
        if node is None:
            return self._next_node
        else:
            self._next_node = node


text = 'One, sentences.   Twho : dsfdsa?! ! dsfdsa ! Ahha cool... No'
#       0             14               31 34       43    49
txt = Text(text)
for a in txt.sentences:
    print a.original()

print '-------------'

for a in txt.sentences.blocks:
    print a.original()

#print '-------------'

#for a in txt.blocks:
#    print '|' + str(a) + '|' + a.original() + '|'
