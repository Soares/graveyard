from ..controllers import Vertical as Controller
from ..shapes import DynamicPair
from .directional import Directional

class Vertical(Directional):
	controller = Controller()

	minimums = lambda self: DynamicPair(*reversed(self._minimums()))
	maximums = lambda self: DynamicPair(*reversed(self._maximums()))
	space = lambda self: DynamicPair(*self._space())

	def draw_spacer_after(self, child):
		from api.line import hline
		hline(self.spacer, child.position.x,
		                   child.position.y + child.position.height,
		                   child.position.width,
		                   self.module.setting('spacers.vertical.color'))
