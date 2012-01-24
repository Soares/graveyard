from ..controllers import Horizontal as Controller
from ..shapes import DynamicPair
from .directional import Directional

class Horizontal(Directional):
	controller = Controller()
	minimums = lambda self: DynamicPair(*self._minimums())
	maximums = lambda self: DynamicPair(*self._maximums())
	space = lambda self: DynamicPair(*self._space())

	def draw_spacer_after(self, child):
		from api.line import vline
		vline(self.spacer, child.position.x + child.position.width,
		                   child.position.y,
		                   child.position.height,
		                   self.module.setting('spacers.horizontal.color'))
