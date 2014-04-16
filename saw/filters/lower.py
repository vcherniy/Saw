class Lower:
    @staticmethod
    def filter(node):
    	new_node = node.copy(lambda x: x.lower())
        return new_node.text(node._text.lower())