from utilities import isclass, isfunc
from utilities.dict import combine
from functools import reduce
from itertools import chain

class Settings:
	fallback = property(lambda self: self.parent if self.inheriting == 'parent' else self.inheriting)
	undefined = object()

	def __init__(self, value=undefined, definitions=None, aliases=None, inheriting=False, **kwargs):
		self.values, self.aliases = definitions or {}, aliases or {}

		# Set the value
		if value != self.undefined:
			self.values[''] = value

		# Check for duplicates
		for name, value in kwargs.items():
			if name in self.values:
				raise ValueError('Settings object given more than one definition for {}'.format(name))
			self.values[name] = value

		# Prepare aliases
		for key, alts in self.aliases.items():
			if key not in self.values:
				raise ValueError('Aliases given for key {} which is not in {}'.format(key, self))
			self.aliases[key] = set([alts] if isinstance(alts, str) else alts)
			overlap = self.aliases[key].intersection(chain(*self.values))
			if overlap:
				raise ValueError('Aliases for {} conflict with existing values: {}'.format(key, overlap))

		# Attach aliases
		tokeys = [{alt: key for alt in alts} for (key, alts) in self.aliases.items()]
		self.aliases = reduce(combine, tokeys, {})

		for name in chain(self.values, self.aliases):
			if '.' in name:
				raise ValueError('Setting values can not have dots in them: {}'.format(name))

		# Initialize the parent and fallback
		self.parent = None
		self.inheriting = inheriting

		# Set the parents of all children
		for name, value in self.values.items():
			if isinstance(value, Settings):
				value.assign(self, name)

	def assign(self, parent, name):
		self.name = name
		self.parent = parent

	def split(self, path):
		name, *rest = path.split('.')
		return self.aliases.get(name, name), '.'.join(rest)

	def retrieve(self, value, *args, **kwargs):
		instantiate = isclass(value) and getattr(value, 'instantiate', False)
		call = isfunc(value) and getattr(value, 'dont_call', True)
		return value(self, *args, **kwargs) if instantiate or call else value

	def overwrite(self, name, value):
		self.values[name] = value

	def get(self, path, *args, **kwargs):
		parent, value = self[path]
		return parent.retrieve(value, *args, **kwargs)

	def set(self, path, value):
		if path not in self:
			raise KeyError('{} not found in {}'.format(path, self))
		self[path] = value

	def child(self, path):
		name, rest = self.split(path)
		if name not in self.values or not isinstance(self.values[name], Settings):
			raise KeyError('Child {} is not present in {}'.format(path, self))
		return self.values[name].child(rest) if rest else self.values[name]

	def __contains__(self, path):
		name, rest = self.split(path)
		if name in self.values:
			next = self.values[name]
			return (rest in next) if isinstance(next, Settings) else (not rest)
		return self.fallback and path in self.fallback

	def __getitem__(self, path):
		name, rest = self.split(path)
		if name in self.values:
			next = self.values[name]
			if not isinstance(next, Settings) and not rest:
				return self, next
			try:
				return next[rest]
			except KeyError:
				pass
		if self.fallback:
			return self.fallback[path]
		raise KeyError('{} not found in {}'.format(path, self))

	def __setitem__(self, path, value):
		name, rest = self.split(path)

		if name not in self.values:
			# Make sure we have a node to talk to
			self.values[name] = Settings()
		elif rest and not isinstance(self.values[name], Settings):
			# If we're going to need to do some walking,
			# make sure that the node is not a leaf
			self.values[name] = Settings(self.values[name])

		if isinstance(self.values[name], Settings):
			self.values[name][rest] = value
		else:
			self.values[name] = value

	def __str__(self):
		return 'Settings' if self.parent is None else '{}.{}'.format(self.parent, self.name)
