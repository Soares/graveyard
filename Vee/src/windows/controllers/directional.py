from itertools import chain
import exceptions
from utilities import ltz
from utilities.itertools import naturals
from ..utilities import shift_left, shift_right, divide
from ..shapes import Pair, Rect, RectDiff, AgnosticPair as APair
from ..nodes.window import Window
from .base import Controller

class Directional(Controller):
	start = lambda self, node: self.order(node.position)[0]
	length = lambda self, node: self.order(node.position)[2]
	describe = lambda self, node: self.order(node.position)[::2]
	padding = lambda self, node: self.order(node.padding)[::2]
	room = lambda self: APair(
		lambda node: self.order(node.room)[0],
		lambda node: self.order(node.room)[1])
	space = lambda self: APair(
		lambda node: self.order(node.space)[0],
		lambda node: self.order(node.space)[1])
	excess = lambda self: APair(
		lambda node: self.order(node.excess)[0],
		lambda node: self.order(node.excess)[1])
	space = lambda self: APair(
		lambda node: self.order(node.space)[0],
		lambda node: self.order(node.space)[1])
	minimums = lambda self: APair(
		lambda node: self.order(node.bounds)[0].min,
		lambda node: self.order(node.bounds)[1].min)
	scale = lambda self, node, amount: node.scale(*self.order(amount))
	shift = lambda self, node, amount: node.shift(*self.order(amount))
	spacer = lambda self, module: module.setting(self._spacer)
	new_window = lambda self, node, manager: Window(manager,
		node.position.x, node.position.y,
		*self._reorder(1, self.order(node.position)[3]))

	def __init__(self, *args, **kwargs):
		super(Directional, self).__init__(*args, **kwargs)
		for initializer in ('room', 'excess', 'space', 'minimums'):
			setattr(self, initializer, getattr(self, initializer)())

	def order(self, object):
		if isinstance(object, int):
			return self._order(object)
		elif isinstance(object, tuple):
			return self._reorder(*list(object))
		elif isinstance(object, Pair):
			return self._reorder(*list(object))
		elif isinstance(object, (Rect, RectDiff)):
			rect = tuple(object)
			primary = self._reorder(*rect[:2])
			secondary = self._reorder(*rect[2:])
			return tuple(chain(primary, secondary))

	def set(self, node, start=None, length=None):
		if start is not None:
			node.move(*self.order(start))
		if length is not None:
			node.resize(*self.order(length))

	def resize(self, node, amount):
		if amount > 0:
			return self.grow(node, amount)
		elif amount < 0:
			return self.shrink(node, -amount)

	def grow_space(self, node):
		m = self.manager(node)
		if not m:
			return 0
		ms, ns = self.excess(node), self.excess(m.direct_child(node))
		return self.grow_space(m) + ms - ns

	def grow(self, node, amount):
		if amount <= 0:
			return
		m = self.manager(node)
		if not m:
			raise exceptions.NotEnoughSpace
		node = m.direct_child(node)
		available = self.excess(m) - self.excess(node)
		self.grow(m, amount - available)
		left, right = self._resize(m, node, min(amount, available))
		self.shift(node, -left)
		self.scale(node, left + right)

	def shrink_space(self, node):
		return self.excess(node)

	def shrink(self, node, amount):
		if self.shrink_space(node) < amount:
			raise exceptions.NotEnoughSpace
		m = self.manager(node)
		if not m or len(m) is 1:
			raise ValueError
		node = m.direct_child(node)
		grower, left, right = self._grower(m, node)
		self.shift(grower, -left * amount)
		self.scale(grower, amount)
		self.scale(node, -amount)
		self.shift(node, right * amount)

	def count(self, node):
		if not len(node):
			return 1
		elif getattr(node, 'controller', None) != self:
			return max(map(self.count, node.active()))
		return sum(map(self.count, node.active()))

	def equalize(self, module):
		sp = len(self.spacer(module))

		def innerreqs(node):
			if not len(node):
				return self.minimums.along(node)
			elif getattr(node, 'controller', None) != self:
				return max(map(innerreqs, node))
			return sum(map(innerreqs, node))

		def allpadding(node):
			padding = sum(self.padding(node))
			if getattr(node, 'controller', None) == self:
				padding += node._len_spacers()
			return padding + (sum(map(allpadding, node)) if len(node) else 0)

		def requirements(node):
			for child in node.active():
				yield (allpadding(child), innerreqs(child), self.count(child))

		def equalize(node, start, amount):
			if not len(node):
				return self.set(node, start, amount)
			pa, pb = self.padding(node)
			start, amount = start + pa, amount - pa - pb
			if getattr(node, 'controller', None) != self:
				for child in node:
					equalize(child, start, amount)
				return
			# [(space and padding, inner requirements, flattened count)]
			reqs = list(requirements(node))
			# Remove the space that we will waste on spacers
			available = amount - node._len_spacers()
			# Remove all of the space that children will waste on spacers
			available -= sum(p for (p, r, c) in reqs)
			# Now we are left with only space used for windows oriented like us
			proposed = list(divide(available, (c for (p, r, c) in reqs)))
			required = [r for (p, r, c) in reqs]
			diffs = [p - r for (p, r) in zip(proposed, required)]
			while any(map(ltz, diffs)):
				negi = next(i for (i, x) in enumerate(diffs) if x < 0)
				posi = max(zip(diffs, naturals()))[0]
				if diffs[posi] <= 0:
					raise exceptions.NotEnoughSpace
				proposed[posi] -= 1
				diffs[posi] -= 1
				proposed[negi] += 1
				diffs[negi] += 1

			for (child, (p, r, c), inner) in zip(node.active(), reqs, proposed):
				equalize(child, start, p + inner)
				start += p + inner + sp

		for child in module.manager:
			equalize(child, self.start(module.manager), self.length(module.manager))

	def _grower(self, manager, node):
		after = manager.after(node)
		return (after, 1, 0) if after else (manager.before(node), 0, 1)

	def _resize(self, node, about, amount):
		right = shift_right(node.afters(about), amount, self.shift, self.scale)
		left = shift_left(reversed(node.befores(about)), amount - right, self.shift, self.scale)
		return left, right
