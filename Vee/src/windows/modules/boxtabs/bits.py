from itertools import chain

class BitList:
	def __init__(self, settings, *bits):
		self.settings, self.bits = settings, bits

	def __iter__(self):
		while not self.bits:
			yield ''

		sep = self.settings.get('separator')
		for strings in zip(*map(iter, self.bits)):
			yield sep.join(strings)

		arrows, numbered = map(self.settings.get, self.arrows)
		numbered = numbered.format(arrows=arrows, n=len(self.bits))
		count = next(filter(lambda b: hasattr(b, 'length'), self.bits)).length
		for i in range(count):
			yield numbered
		for i in range(count):
			yield arrows
		while True:
			yield ''


class Befores(BitList):
	arrows = '«', '«n'


class Afters(BitList):
	arrows = '»', 'n»'


class Bit:
	def __init__(self, node):
		self.node = node
		self.length = len(list(node.names()))

	def __iter__(self):
		return self.node.names()


class SelectedBit(Bit):
	def __iter__(self):
		names = tuple(self.node.names())
		# full, numbered arrows, arrows, alone
		return chain(names, names, names, names)


class BitSet:
	def __init__(self, left, selected, right):
		self.parts = (left, selected, right)

	def __iter__(self):
		return zip(*map(iter, self.parts))
