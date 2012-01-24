from api.canvas import Canvas
from .base import Node
from ..shapes import DynamicPair, DynamicRect

class Window(Node):
	inner = lambda self: DynamicRect(
		lambda: self.canvas.x, lambda: self.canvas.y,
		lambda: self.canvas.width, lambda: self.canvas.height)
	minimums = lambda self: DynamicPair(
		lambda: self.module.setting('constraints.min.width', self),
		lambda: self.module.setting('constraints.min.height', self))
	maximums = lambda self: DynamicPair(
		lambda: self.module.setting('constraints.max.width', self),
		lambda: self.module.setting('constraints.max.height', self))
	space = lambda self: DynamicPair(
		lambda: self.excess.width,
		lambda: self.excess.height)

	def current(self):
		return self

	def __init__(self, manager, x, y, width, height):
		super(Window, self).__init__(manager)
		self.canvas = Canvas(x, y, width, height)

	def __len__(self):
		return 0

	def __bool__(self):
		return True

	def _refresh(self):
		self.canvas.redraw()

	def move(self, x, y):
		self.canvas.move(x, y)

	def resize(self, width, height):
		self.canvas.resize(width, height)

	def close(self):
		self._discard()

	def count(self):
		return 1

	def names(self):
		full = str(self)
		yield ' ' + full + ' '
		yield ' ' + full[:8] + ' '
		yield ' ' + full[:5] + ' '
		yield ' ' + full[:3] + ' '
		yield ' ' + full[:1] + ' '
		yield full[:1] + ' '
		yield full[:1]
		yield '-'

	def __str__(self):
		return str(self.canvas)
