from api.style import color
from api.compatability import unicode
from module import Module
from .nodes import WindowManager
from settings import Settings

class Windows(Module):
	from .modules import boxtabs
	submodules = (boxtabs.BoxTabs,)
	settings = Settings(
		spacers=Settings(
			color=color('disabled'),
			horizontal=Settings('|',
				color=lambda s: s.parent.get('color')),
			vertical=Settings('-',
				color=lambda s: s.parent.get('color'))),
		constraints=Settings(
			min=Settings(
				width=Settings(lambda s, window: 1 if window.is_selected() else 0),
				height=Settings(lambda s, window: 1 if window.is_selected() else 0)),
			max=Settings(
				width=Settings(None),
				height=Settings(None))),
		tab=Settings(
			arrows=Settings(
				before=Settings(unicode('«', '<<'),
					numbered='{arrows} {n}',
					aliases={'numbered': '«n'}),
				after=Settings(unicode('»', '>>'),
					numbered='{n} {arrows}',
					aliases={'numbered': 'n»'}),
				aliases={'before': '«', 'after': '»'})))
	current = property(lambda self: self.manager.current())

	def connections(self):
		from core.signals import update
		return [(update, self.update, self.parent)]

	def update(self, **kwargs):
		self.current.canvas.take_cursor()

	def setup(self):
		x, y, w, h = self.parent.x(), self.parent.y(), self.parent.width(), self.parent.height()
		self.manager = WindowManager(self, x, y, w, h)
