"""Mite multi-compiler generator."""
import itertools

from mite import Misconfigured
from mite.compiler.base import Stripped


def multipiler(compilers):
	"""
	Generates a class that does mulitple compiler actions in sequence.
	Useful if you have a compiler type that generates tags or something.
	"""
	compilers = list(compilers)
	if not compilers:
		raise Misconfigured('Cannot have empty compiler list.')

	class MultiCompiler(Stripped):
		"""Does multiple compiler actions."""

		def __init__(self, name, config):
			# Initializers mutate the config.
			super().__init__(name, dict(config))
			self._compilers = [c(name, dict(config)) for c in compilers]

		@property
		def compilers(self):
			return self._compilers

		def filters(self, *args, **kwargs):
			return itertools.chain(*(c.filters(*args, **kwargs).items()
				for c in self.compilers))

		def globals(self, *args, **kwargs):
			return dict(itertools.chain(*(c.globals(*args, **kwargs).items()
				for c in self.compilers)))

		def loaders(self, *args, **kwargs):
			return itertools.chain(*(c.loaders(*args, **kwargs)
				for c in self.compilers))

		def initialize(self, *args, **kwargs):
			for compiler in self.compilers:
				compiler.initialize(*args, **kwargs)

		def compile(self, *args, **kwargs):
			for compiler in self.compilers:
				compiler.compile(*args, **kwargs)

		def remove(self):
			for compiler in self.compilers:
				compiler.remove(*args, **kwargs)

	return MultiCompiler
