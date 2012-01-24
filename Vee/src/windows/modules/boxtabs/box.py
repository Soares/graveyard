from api.line import vline, hline, Line
from .windows.nodes import Tabular
from .bits import Bit, BitSet, Befores, Afters, SelectedBit

class Boxer:
	def __init__(self, settings):
		self.settings = settings

	def pads(self):
		left = len(self.settings.get('lines.left'))
		above = 1 + len(self.settings.get('lines.above'))
		right = len(self.settings.get('lines.right'))
		below = len(self.settings.get('lines.below'))
		return left, above, right, below

	def rebox(self, node):
		if getattr(node, 'boxer', self) != self:
			node.boxer.unbox(node)
			self.box(node)
		self.draw(node)

	def box(self, node):
		node.inner.pad(*self.pads())
		node.boxer = self

	def unbox(self, node):
		del node.boxer
		node.inner.pad(*(-x for x in self.pads()))

	def is_active(self, node):
		return Tabular.controller.manager(node.module.current) == node

	def draw(self, node):
		left = self.settings.get('lines.left')
		right = self.settings.get('lines.right')
		below = self.settings.get('lines.below')
		bg = self.settings.get('colors.background', node)
		vline(left, node.position.x, node.position.y, node.position.height, bg)
		vline(right, node.inner.x + node.inner.width, node.position.y, node.position.height, bg)
		hline(below, node.position.x, node.inner.y + node.inner.height, node.position.width, bg)
		self.bar(node)
	
	def bar(self, node):
		above = self.settings.get('lines.above')
		sep = self.settings.get('separator')
		bg = self.settings.get('colors.background', node)
		con = self.settings.get('colors.selected', node)
		coff = self.settings.get('colors.deselected', node)

		hline(above, node.inner.x, node.position.y + 1, node.inner.width, bg)

		bitlist = BitSet(
			Befores(self.settings, *map(Bit, node.befores(node.selected))),
			SelectedBit(node.selected),
			Afters(self.settings, *map(Bit, node.afters(node.selected))))
		seplen, width = len(sep), node.inner.width
		for (before, selected, after) in bitlist:
			lb, ls, la =len(before), len(selected), len(after)
			if lb + (seplen if lb else 0) + ls + (seplen if la else 0) + la <= width:
				break
		line = Line(node.inner.x, node.position.y, node.inner.width, bg)
		line.add(before, coff)
		if before: line.add(sep, coff)
		line.add(selected, con)
		if after: line.add(sep, coff)
		line.add(after, coff)
		line.draw()


class Barrer(Boxer):
	def is_active(self, node):
		return self.settings.get('active') == node

	def box(self, node):
		if self.settings.get('active') is None:
			self.settings.set('active', node)
		return super(Barrer, self).box(node)
