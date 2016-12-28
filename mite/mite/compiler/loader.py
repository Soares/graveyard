"""Mite compiler loading."""
import os
import imp
import logging

from mite import Misconfigured
from mite.compiler.list import multipiler
from mite.compiler.copy import Copier
from mite.compiler.flow import Flow

BUILTIN = {
	'copy': Copier,
	'flow': Flow,
}


class Loader:
	def __init__(self, fallback, directory):
		assert os.path.isdir(directory)
		self.directory = directory
		self.fallback = fallback
		self._cache = dict(BUILTIN)

	def load(self, name, config):
		"""Creates a module using the compiler specified in config."""
		if not os.path.isdir(name):
			raise Misconfigured('{} directory not found.'.format(name))
		cls = self.compiler(config.pop('compiler', None), name)
		return cls(name, config)

	def compiler(self, compiler, module):
		"""
		Gets a compiler class.
		If compiler is None, a compiler with a name matching the module will be
		searched for. If no compiler can be found, the fallback will be used.
		"""
		if isinstance(compiler, list):
			return multipiler(self.compiler(c, module) for c in compiler)
		if compiler is None:
			samename = os.path.join(self.directory, module + '.py')
			if os.path.exists(samename):
				compiler = module
		if compiler is None:
			logging.debug(
					'%s will use fallback compiler %s', module, self.fallback)
			compiler = self.fallback
		if compiler not in self._cache:
			path = os.path.join(self.directory, compiler + '.py')
			if not os.path.exists(path):
				raise Misconfigured(
						"Couldn't find compiler: {}"
						" (should be at {})".format(compiler, path))
			logging.debug('loading %s compiler from %s', module, path)
			import mite.compiler  # Suppresses imp warnings.
			name = 'mite.compiler.{}'.format(compiler)
			module = imp.load_source(name, path)
			if not hasattr(module, 'Compiler'):
				raise Misconfigured('{} has no Compiler class.'.format(path))
			self._cache[compiler] = module.Compiler
		return self._cache[compiler]
