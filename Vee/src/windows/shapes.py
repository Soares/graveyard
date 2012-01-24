from operator import getitem
from utilities import do
from utilities.list import expose as expose_list
import exceptions

class MetaShape(type):
	def __init__(self, *args, **kwargs):
		super(MetaShape, self).__init__(*args, **kwargs)
		def attach(pair):
			i, name = pair
			def get(instance): return instance[i]
			def set(instance, value): instance[i] = value
			attr = property(get) if self._dynamic else property(get, set)
			setattr(self, name, attr)
		if hasattr(self, '_names'):
			do(attach, enumerate(self._names))
		if self._dynamic:
			self.__getitem__ = lambda self, *a, **kw: getitem(self._attrs, *a, **kw)()


@expose_list('_attrs')
class Shape(metaclass=MetaShape):
	_dynamic = False
	_default = 0

	def __init__(self, *attrs):
		self._attrs = list(attrs)
		while len(self._attrs) < len(self._names):
			self._attrs.append(self._default)

	def __repr__(self):
		attrs = ' '.join('{}={}'.format(name, getattr(self, name)) for name in self._names)
		return '<{}: {}>'.format(self.__class__.__name__, attrs)


class Pair(Shape):
	_names = 'width', 'height'


class DynamicPair(Pair):
	_dynamic = True


class AgnosticPair(Shape):
	_names = 'along', 'against'


class AgnosticDynamicPair(AgnosticPair):
	_dynamic = True


class Constraint(Shape):
	_default = None
	_names = 'min', 'max'


class DynamicConstraint(Constraint):
	_dynamic = True


class Rect(Shape):
	_names = 'x', 'y', 'width', 'height'

	left = property(lambda self: self.x)
	right = property(lambda self: self.left + self.width - 1)
	above = property(lambda self: self.y)
	below = property(lambda self: self.above + self.height - 1)

	def clamp(self, x, y):
		x = max(self.left, min(self.right, x))
		y = max(self.above, min(self.below, y))
		return x, y

	def contains(self, x, y):
		return self.left <= x <= self.right and self.above <= y <= self.below


class DynamicRect(Rect):
	_dynamic = True


class ListNodeRect(DynamicRect):
	def __init__(self, node, *attrs):
		self.node = node
		super(ListNodeRect, self).__init__(*attrs)

	def pad(self, left, above, right, below):
		from .nodes import Horizontal, Vertical

		dw, dh = -(left + right), -(above + below)

		mw, mh = self.node.maximums.width, self.node.maximums.height
		mw = (mw - self.node.inner.width) if mw is not None else dw
		mh = (mh - self.node.inner.height) if mh is not None else dh

		ew, eh = self.node.module.manager.excess
		sw, sh = self.node.minimums
		sw -= self.node.inner.width
		sh -= self.node.inner.height

		if dw > mw or dh > mh:
			raise exceptions.NotEnoughSpace
		elif -dw > ew or -dh > eh:
			raise exceptions.NotEnoughSpace

		self.node.padding.left += left
		self.node.padding.above += above
		self.node.padding.right += right
		self.node.padding.below += below

		if dw < sw and dh < sh:
			Horizontal.controller.equalize(node.module)
			Vertical.controller.equalize(node.module)
		elif dw < sw:
			Horizontal.controller.equalize(node.module)
			for child in self.node:
				child.scale(None, dh)
				child.shift(None, above)
		elif dh < sh:
			Vertical.controller.equalize(node.module)
			for child in self.node:
				child.scale(dw, None)
				child.shift(left, None)
		else:
			for child in self.node:
				child.scale(dw, dh)
				child.shift(left, above)
		self.node.refresh()


class RectDiff(Shape):
	_names = 'left', 'above', 'right', 'below'
