import exceptions
from utilities import fallback
from ..utilities import shift_left
from .base import ListNode

class Directional(ListNode):
	_len_spacers = lambda self: len(self.spacer) * (len(self) - 1)
	_minimums = lambda self: (
		lambda: sum(map(self.controller.minimums.along, self)) + self._len_spacers(),
		lambda: max(map(self.controller.minimums.against, self)))
	_maximums = lambda self: (
		lambda: fallback(lambda: sum(map(self.controller.room.along, self)), TypeError, None),
		lambda: fallback(lambda: sum(map(self.controller.room.against, self)), TypeError, None))
	_space = lambda self: (
		lambda: sum(map(self.controller.space.along, self.active())),
		lambda: max(map(self.controller.space.against, self.active())))
	spacer = property(lambda self: self.controller.spacer(self.module))

	def scale(self, dw, dh):
		da, db = self._enforce_bounds(dw, dh)
		if db:
			for child in self:
				self.controller.scale(child, db)
		if da and da > 0:
			self.controller.scale(self[-1], da)
		elif da and da < 0:
			shift = self.controller.shift
			scale = self.controller.scale
			shift_left(reversed(self), -da, shift, scale)

	def select_near(self, x, y, *args, **kwargs):
		super(Directional, self).select_near(x, y, *args, **kwargs)
		self.selected._select(x, y)

	def _refresh(self):
		for child in self[:-1]:
			self.draw_spacer_after(child)
			child.refresh()
		self[-1].refresh()

	def _add(self, node, after=None):
		self._ensure_space_for(node)
		self.insert(node, after=after)
		self.controller.equalize(self.module)

	def _shut(self, node):
		self._ensure_roomage_for(node)
		self.remove(node)
		self.controller.equalize(self.module)

	def _ensure_space_for(self, node):
		available = self.controller.space.along(self.module.manager)
		required = self.controller.minimums.along(node) + len(self.spacer)
		if available < required:
			raise exceptions.NotEnoughSpace(available, required)

	def _ensure_roomage_for(self, node):
		# Max amount that this window can grow (None if unbounded)
		roomage = self.controller.room.along(self)
		if roomage is None:
			return

		cmax = self.constraints.width.max
		if cmax is None or cmax > self.maximums.width:
			# We are constrained by each and every child, not by user constraints
			# The node that we are removing can not be expanded, discount its roomage
			roomage -= self.controller.room.along(node)

		required = self.controller.length(node) + len(self.spacer)
		if roomage < required:
			raise exceptions.NotEnoughSpace(roomage, required)

	def _enforce_bounds(self, dw, dh):
		# Delta a, Delta b
		da, db = self.controller.order((dw, dh))

		# Room to grow a, Room to grow b
		ra, rb = self.controller.order(self.room)
		if ra is None: ra = da
		if rb is None: rb = db

		# Room to shrink a, Room to shrink b
		ea, eb = self.controller.order(self.excess)
		sa, sb = -ea, -eb

		if da < sa or db < sb or da > ra or db > rb:
			raise exceptions.NotEnoughSpace
		return da, db
