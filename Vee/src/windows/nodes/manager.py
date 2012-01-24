from .base import Node
from .window import Window
from ..shapes import DynamicPair, Rect

class WindowManager(Node):
	inner = lambda self: Rect()
	minimums = lambda self: DynamicPair(
		lambda: self.child.bounds.width.min, lambda: self.child.bounds.height.min)
	maximums = lambda self: DynamicPair(
		lambda: self.child.bounds.width.min, lambda: self.child.bounds.height.min)
	space = lambda self: DynamicPair(
		lambda: self.child.space.width, lambda: self.child.space.height)
	selected = property(lambda self: self.child)

	def __init__(self, module, x, y, width, height):
		super(WindowManager, self).__init__(None)
		self.module = module
		self.inner.x, self.inner.y, self.inner.width, self.inner.height = x, y, width, height
		self.child = Window(self, x, y, width, height)

	def active(self):
		return [self.child]

	def __iter__(self):
		return iter([self.child])

	def __len__(self):
		return 1

	def is_selected(self):
		return True

	def scale(self, dw, dh):
		self.child.scale(dw, dh)
		self.inner.width += dw
		self.inner.height += dh

	def shift(self, dx, dy):
		self.child.shift(dx, dy)
		self.inner.x += dx
		self.inner.y += dy

	def close(self):
		self.child.close()
		super(WindowManager, self).close()

	def current(self):
		return self.child.current()
	
	def encapsulate(self, into, node):
		assert node == self.child
		self.child = into(self, node)
		return self.child

	def merge(self, node):
		assert node == self.child
		assert len(node) is 1
		self.child = node[0]
		self.child.manager = self
		node._discard()

	def count(self):
		return self.child.count()

	def _refresh(self):
		self.child.refresh()

	def names(self):
		return self.child.names()

	def __str__(self):
		return '<{}>'.format(self.child)
