from operator import add, sub
import exceptions
from utilities.list import expose as expose_list
from utilities import iff, laxmin, laxmax
from ..shapes import Pair, DynamicPair
from ..shapes import Constraint, DynamicConstraint
from ..shapes import RectDiff, DynamicRect, ListNodeRect

class Node:
	# maximums = lambda self: Constraint(...)
	# minimums = lambda self: Constraint(...)
	# inner = lambda self: Rect(...)
	constraints = lambda self: Pair(Constraint(), Constraint())
	bounds = lambda self: Pair(
	    DynamicConstraint(
	        lambda: laxmax(self.constraints.width.min,
	                       self.minimums.width + self.padding.left + self.padding.right),
	        lambda: laxmin(self.constraints.width.max, self.maximums.width)),
	    DynamicConstraint(
	        lambda: laxmax(self.constraints.height.min,
	                       self.minimums.height + self.padding.above + self.padding.below),
			lambda: laxmin(self.constraints.height.max, self.maximums.height)))
	room = lambda self: DynamicPair(
	    lambda: iff(self.bounds.width.max, sub, self.position.width),
	    lambda: iff(self.bounds.height.max, sub, self.position.height))
	excess = lambda self: DynamicPair(
	    lambda: self.position.width - self.bounds.width.min,
	    lambda: self.position.height - self.bounds.height.min)
	padding = lambda self: RectDiff()
	position = lambda self: DynamicRect(
	    lambda: self.inner.x - self.padding.left,
	    lambda: self.inner.y - self.padding.above,
	    lambda: self.inner.width + self.padding.left + self.padding.right,
	    lambda: self.inner.height + self.padding.above + self.padding.below)

	def __init__(self, manager):
		self.manager = manager
		for initializer in ('inner', 'minimums', 'maximums', 'bounds', 'room',
							'space', 'excess', 'padding', 'position', 'constraints'):
			setattr(self, initializer, getattr(self, initializer)())
		if manager:
			self.module = manager.module

	def is_selected(self):
		return self.manager.selected == self and self.manager.is_selected()

	def shift(self, dx, dy):
		self.move(iff(dx, add, self.position.x), iff(dy, add, self.position.y))

	def scale(self, dw, dh):
		self.resize(iff(dw, add, self.position.width), iff(dh, add, self.position.height))

	def move(self, x, y):
		self.shift(iff(x, sub, self.position.x), iff(y, sub, self.position.y))

	def resize(self, width, height):
		self.scale(iff(width, sub, self.position.width), iff(height, sub, self.position.height))

	def close(self):
		"""Close this node and any child nodes it may have."""
		self._discard()

	def refresh(self):
		from ..signals import refreshing, refreshed
		refreshing.send(self.__class__, instance=self)
		self._refresh()
		refreshed.send(self.__class__, instance=self)

	def _discard(self):
		"""Dispose of this node, but don't touch any child nodes"""
		pass

	def _select(self, x, y):
		"""Change selection to match given cursor position"""
		pass


@expose_list('_children')
class ListNode(Node):
	selected = property(
		lambda self: self[self.index],
		lambda self, node: setattr(self, 'index', self._index(node)))
	inner = lambda self: ListNodeRect(self,
		lambda: min(c.position.x for c in self),
		lambda: min(c.position.y for c in self),
		lambda: max(c.position.x + c.position.width for c in self) - self.inner.x,
		lambda: max(c.position.y + c.position.height for c in self) - self.inner.y)

	def __init__(self, manager, *children):
		super(ListNode, self).__init__(manager)
		self._children, self.index = list(children), 0
		for child in self:
			child.manager = self
	
	def shift(self, dx, dy):
		"""Shift the whole window and all children"""
		for child in self:
			child.shift(dx, dy)

	def move(self, x, y):
		super(ListNode, self).move(x + self.padding.left, y + self.padding.above)

	def active(self):
		"""Child windows that are currently visible"""
		return iter(self)

	def current(self):
		"""The currently selected (lowest level) window"""
		return self.selected.current()

	def direct_child(self, node):
		"""Find the immediate child (in this list) which is ancestor of descendant 'node'"""
		if node in self:
			return node
		elif node.manager == node:
			raise IndexError
		return self.direct_child(node.manager)

	def before(self, node):
		"""The window immediately before 'node' in the list or None"""
		return self._near(node, -1)

	def after(self, node):
		"""The window immediately after 'node' in the list or None"""
		return self._near(node, 1)

	def befores(self, node):
		"""All windows before 'node' in the list"""
		index = self._children.index(node)
		return self[:index]

	def afters(self, node):
		"""All windows after 'node' in the list"""
		index = self._children.index(node)
		return self[index+1:]

	def select_near(self, x, y, direction):
		"""Move the selection forward or backward one window"""
		assert direction in (1, -1)
		index = self.index + direction
		if index >= len(self) or index < 0:
			raise exceptions.OutOfBounds
		self.index = index

	def add(self, node, after=None):
		"""Add a window and shift the other windows to make it fit"""
		return self._add(node, after)

	def insert(self, node, after=None):
		"""Insert a window into the list. Do not shift other windows."""
		after = after or self[-1]
		index = self._index(after) + 1
		self._children.insert(index, node)
		node.manager = self

	def shut(self, node):
		"""Close a window and shift the other windows to make it fit"""
		if len(self) is 1:
			raise exceptions.OutOfBounds
		return self._shut(node)

	def remove(self, node):
		"""Remove a window from the list. Do not shift other windows."""
		if node not in self:
			raise ValueError
		self._children.remove(node)
		node.close()
		if self.index >= len(self):
			self.index = len(self) - 1

	def close(self):
		"""Close this node, preparing for being discarded"""
		for child in self:
			child.close()
		super(ListNode, self).close()

	def replace(self, node1, node2):
		"""Swap two windows. The removed window will not be closed, but rather returned."""
		index = self._index(node1)
		self[index] = node2
		return node1

	def merge(self, node):
		"""
		Replace a list node with the contents of the list.
		The old container will be discarded.
		"""
		index = self._index(node)
		node = self._children.pop(index)
		for n in reversed(node):
			n.manager = self
			self._children.insert(index, n)
		node._discard()
	
	def encapsulate(self, into, *nodes):
		"""
		Replace '*nodes' with an instance of 'into' containing '*nodes'.
		The resulting node will be inserted in the position of the last
		node in '*nodes'.
		"""
		popped = []
		for n in nodes:
			index = self._children.index(n)
			popped.append(self._children.pop(index))
		new = into(self, *popped)
		self._children.insert(index, new)
		return new

	def count(self):
		"""
		The total number lowest-level windows in this node and in
		all of this node's children
		"""
		return sum(c.count() for c in self)

	def _select(self, x, y):
		x, y = self.inner.clamp(x, y)
		for child in self:
			if child.position.contains(x, y):
				self.selected = child
				child._select(x, y)
				break

	def _index(self, node):
		"""Find the index of 'node' in this node (or raise ValueError)"""
		if node not in self:
			raise ValueError
		return self._children.index(node)

	def _near(self, node, direction):
		"""Find a node near 'node' or return None"""
		index = self._children.index(node)
		try:
			return self[index + direction]
		except IndexError:
			return None

	def names(self):
		"""
		The names that should be used to reference this list node,
		in order from verbose to single character
		"""
		current = self.current()
		def annotated():
			count = str(self.count())
			for name in list(current.names())[:-2]:
				yield '{}:{}'.format(count, name.lstrip())
			yield count + ' '
			yield '-'
		return current.names() if len(self) is 1 else annotated()

	def __str__(self):
		return '<{} {{{}}}>'.format(self.__class__.__name__, ', '.join(map(str, self)))
