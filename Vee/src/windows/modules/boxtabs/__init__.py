import exceptions
from settings import Settings
from module import Module
from api.style import color
from .windows.nodes import Vertical, Horizontal, Tabular
from .box import Boxer, Barrer

def is_descendant(node):
	if node.manager is None:
		return True
	if getattr(node, 'controller', None) != Tabular.controller:
		return False
	return is_descendant(node.manager)


def is_active(node):
	if not hasattr(node, 'boxer'):
		return False
	return node.boxer.is_active(node)


class BoxTabs(Module):
	settings = Settings(
		separator='',
		lines=Settings(left=' ', above='', right=' ', below=' '),
		colors=Settings(
			selected=lambda s, t: color('normal' if is_active(t) else 'disabled'),
			background=lambda s, t: color('flashy' if is_active(t) else 'disabled'),
			deselected=lambda s, t: color('flashy' if is_active(t) else 'disabled')),
		bar=Settings(inheriting='parent',
			active=None,
			lines=Settings(left='', right='', below='')))

	def setup(self):
		self.boxer = Boxer(self.settings)
		self.barrer = Barrer(self.settings.child('bar'))

	def boxer_for(self, node):
		return self.barrer if is_descendant(node) else self.boxer

	def connections(self):
		from .windows import signals
		return (
			(signals.splitting, self.check, Tabular),
			(signals.split, self.split, Tabular),
			(signals.closed, self.shrink, Tabular),
			(signals.selected, self.select, Vertical),
			(signals.selected, self.select, Horizontal),
			(signals.refreshed, self.update, Tabular))

	def check(self, manager, node, **kwargs):
		if manager: return
		top = self.parent.manager
		vspace, hspace = top.space
		left, right, above, below = self.boxer_for(node).pads()
		if vspace < (above + below) or hspace < (left + right):
			raise exceptions.NotEnoughSpace(message='There is not enough room to open a new tab.')

	def split(self, manager, **kwargs):
		if manager and len(manager) is 2:
			self.boxer_for(manager).box(manager)

	def shrink(self, manager, **kwargs):
		if len(manager) is 1:
			manager.boxer.unbox(manager)

	def select(self, manager, **kwargs):
		self.parent.manager.refresh()

	def update(self, instance, **kwargs):
		self.boxer_for(instance).rebox(instance)
