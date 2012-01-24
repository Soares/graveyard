from api import Root
from .signals import update, dispatch

class Vee(Root):
	modules = {}

	def setup(self):
		import config
		config.configure(self)

	def dispatch(self, char):
		dispatch.send(self, char=char)

	def update(self, *args, **kwargs):
		update.send(self)
		super(Vee, self).update(*args, **kwargs)
