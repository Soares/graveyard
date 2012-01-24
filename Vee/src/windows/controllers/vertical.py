from .directional import Directional

class Vertical(Directional):
	_order = lambda self, y: (None, y)
	_reorder = lambda self, x, y: (y, x)
	_spacer = 'spacers.vertical'
