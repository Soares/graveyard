from .decorators import class_decorator

@class_decorator
def expose(cls, attr):
	def attach(name):
		name = '__{}__'.format(name)
		fn = lambda s, *a, **kw: getattr(getattr(s, attr), name)(*a, **kw)
		setattr(cls, name, fn)
	for name in ('len', 'getitem', 'setitem', 'reversed', 'contains'):
		attach(name)
	return cls
