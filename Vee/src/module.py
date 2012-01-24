class Module:
	name = property(lambda self: self.__class__.__name__.lower())
	submodules = ()
	modules = {}

	def __init__(self, parent):
		self.parent = parent
		self.setup()
		self.connect()

	def connections(self):
		return ()

	def setup(self):
		pass

	def connect(self):
		for signal, receiver, sender in self.connections():
			signal.connect(receiver, sender, weak=False)

	def disconnect(self):
		for signal, receiver, sender in self.connections():
			signal.disconnect(receiver, sender)

	def setting(self, path='', *args, **kwargs):
		try:
			return self.settings.get(path, *args, **kwargs)
		except KeyError as e:
			name, *path = path.split('.')
			if name not in self.modules:
				raise KeyError('Module {} not found in {}'.format(name, self)) from e
			return self.modules[name].setting('.'.join(path), *args, **kwargs)

	def set(self, path, *args, **kwargs):
		try:
			return self.settings.set(path, *args, **kwargs)
		except KeyError:
			name, *path = path.split('.')
			return self.modules[name].set('.'.join(path), *args, **kwargs)

	def __str__(self):
		return self.name

	@classmethod
	def attach(cls, parent):
		instance = cls(parent)
		parent.modules[instance.name] = instance

		for module in cls.submodules:
			module.attach(instance)

	@classmethod
	def detach(cls, parent, name):
		instance = parent.modules[name]

		for module in cls.submodules:
			module.detach(instance)

		instance.disconnect()
		del parent.modules[name]
