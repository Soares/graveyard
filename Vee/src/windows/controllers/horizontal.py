from .directional import Directional

class Horizontal(Directional):
	_order = lambda self, x: (x, None)
	_reorder = lambda self, x, y: (x, y)
	_spacer = 'spacers.horizontal'
