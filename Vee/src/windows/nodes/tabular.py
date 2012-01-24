from utilities import laxmin
from ..controllers import Tabular as Controller
from ..shapes import DynamicPair
from .base import ListNode

class Tabular(ListNode):
	controller = Controller()
	minimums = lambda self: DynamicPair(
		lambda: max(child.bounds.width.min for child in self),
		lambda: max(child.bounds.height.min for child in self))
	maximums = lambda self: DynamicPair(
		lambda: laxmin(*(child.bounds.width.max for child in self)),
		lambda: laxmin(*(child.bounds.height.max for child in self)))
	space = lambda self: DynamicPair(
		lambda: sum(c.space.width for c in self.active()),
		lambda: sum(c.space.height for c in self.active()))

	def scale(self, dw, dh):
		for child in self:
			child.scale(dw, dh)

	def select_near(self, *args, **kwargs):
		super(Tabular, self).select_near(*args, **kwargs)
		self.refresh()

	def active(self):
		return [self.selected]

	def _add(self, node, after=None):
		self.insert(node, after=after)

	def _shut(self, node):
		self.remove(node)

	def _refresh(self):
		self.selected.refresh()
