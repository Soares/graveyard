import exceptions
from . import signals
from .nodes import Horizontal, Vertical, Tabular


def swap(window1, window2):
	try:
		_match_size(window1, window2)
	except exceptions.NotEnoughSpace:
		_match_size(window2, window1)
	window1.manager.replace(window1, window2)
	window2.manager.replace(window2, window1)
	x, y = window1.x, window1.y
	window1.move(window2.x, window2.y)
	window2.move(x, y)


def close(window):
	if window.manager is None:
		raise exceptions.OutOfBounds("You can't close the last window")
	if len(window.manager) is 1:
		window.manager.manager.merge(window.manager)
		close(window)
	else:
		manager = window.manager
		signals.closing.send(manager.__class__, manager=manager, node=window)
		manager.shut(window)
		signals.closed.send(manager.__class__, manager=manager)
		if len(manager) is 1:
			manager.manager.merge(manager)
		window.module.manager.refresh()


def hsplit(window):
	_split(window, Horizontal)
def vsplit(window):
	_split(window, Vertical)
def tsplit(window):
	_split(window, Tabular)
def _split(window, cls):
	ctrl = cls.controller
	if getattr(window.manager, 'controller', None) == ctrl:
		signals.splitting.send(cls, manager=window.manager, node=window)
		new = ctrl.new_window(window, window.manager)
		window.manager.add(new)
		signals.split.send(cls, manager=window.manager, node=window, new=new)
	else:
		signals.splitting.send(cls, manager=None, node=window)
		manager, new = ctrl.split(cls, window)
		signals.split.send(cls, manager=manager, node=window, new=new)
	window.module.manager.refresh()


def hnext(window):
	_shift(window, Horizontal, 1)
def hprev(window):
	_shift(window, Horizontal, -1)
def vnext(window):
	_shift(window, Vertical, 1)
def vprev(window):
	_shift(window, Vertical, -1)
def tnext(window):
	_shift(window, Tabular, 1)
def tprev(window):
	_shift(window, Tabular, -1)
def _shift(window, cls, direction):
	m = cls.controller.manager(window)
	signals.selecting.send(cls, manager=m, node=window)
	try:
		cls.controller.select_near(window, direction)
	except exceptions.OutOfBounds:
		pass
	signals.selected.send(cls, manager=m, node=window)


def _match_size(master, resizer):
	dw = master.width - resizer.width
	h, v = Horizontal.controller, Vertical.controller
	if h.grow_space(resizer) < dw or h.shrink_space(resizer) < -dw:
		raise exceptions.NotEnoughSpace
	dh = master.height - resizer.height
	if v.grow_space(resizer) < dh or v.shrink_space(resizer) < -dh:
		raise exceptions.NotEnoughSpace
	h.resize(resizer, dw)
	v.resize(resizer, dh)
