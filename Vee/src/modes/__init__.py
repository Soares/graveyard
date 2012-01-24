from module import Module
from settings import Settings
from .normal import Normal

class Modes(Module):
	settings = Settings(default=Normal)
	current = property(lambda self: self.stack[-1])

	def connections(self):
		from core.signals import dispatch
		return [(dispatch, self.dispatch, self.parent)]

	def setup(self):
		self.stack = [self.setting('default')(self.parent)]

	def dispatch(self, char, **kwargs):
		self.current.dispatch(char)
