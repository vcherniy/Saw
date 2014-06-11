class Call:
	@staticmethod
	def filter(node, func):
		return node.copy(func)