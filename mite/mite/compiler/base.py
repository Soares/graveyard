"""Mite module manager."""
import abc
import logging
import os


from mite.compiler.filter import module_url, module_context
import mite.util.path


class Stripped(metaclass=abc.ABCMeta):
	"""The bare bones of Compiler, barely useful for anything."""

	extension = None

	def __init__(self, name, config):
		self.__destroot = config.pop('to', name)
		self.extension = config.pop('extension', self.extension)
		if self.extension and not self.extension.startswith('.'):
			self.extension = '.' + self.extension
		self.__name = name

	@property
	def name(self):
		"""
		The name of the module (which is also its directory in the source tree).
		"""
		return self.__name

	@property
	def destroot(self):
		"""The directory of the module within the build dir."""
		return self.__destroot

	@abc.abstractmethod
	def globals(self, view):
		"""A dict of global variables for any jinja-rendered pages."""

	@abc.abstractmethod
	def filters(self, view):
		"""A dict of global filters for any jinja-rendered pages."""

	@abc.abstractmethod
	def loaders(self, view):
		"""
		An iterable of jinja loaders for the jinja environment.
		Return (jinja2.Loader.FileSystemLoader(self.name),) to enable jinja
		rendering of this module's files directly.
		"""

	@abc.abstractmethod
	def initialize(self, view):
		"""
		Initializes a single filepath.
		See mite.sourcetree.views.Initializing for available actions.
		"""

	@abc.abstractmethod
	def compile(self, view):
		"""
		Compiles a single filepath.
		See mite.sourcetree.views.Compiling for available actions.
		"""

	@abc.abstractmethod
	def remove(self, view):
		"""
		Removes a single filepath.
		See mite.sourcetree.views.Removing for avialable actions.
		"""


class Compiler(Stripped, metaclass=abc.ABCMeta):
	"""
	User-configured module.
	Specifies the compilation of a directory in the site source.
	"""

	def globals(self):
		return {}

	def filters(self):
		return {}

	def loaders(self):
		return ()

	def initialize(self, view):
		super().initialize(view)
		os.makedirs(os.path.dirname(view.destination), exist_ok=True)

	def remove(self, view):
		logging.info('Removing %s', view.url)
		if os.path.exists(view.destination):
			os.remove(view.destination)


class Contained(Compiler, metaclass=abc.ABCMeta):
	"""Superclass for self-contained compilers."""

	def __init__(self, name, config):
		super().__init__(name, config)
		self.pages = set()
		for key in config.keys():
			raise Misconfigured('Unrecognized setting: %s' % key)

	def initialize(self, view):
		super().initialize(view)
		self.pages.add(view.url)

	@abc.abstractmethod
	def compile(self, view):
		super().compile(view)
		if view.url not in self.pages:
			self.initialize(view)

	def filters(self):
		urlroot = mite.util.path.urlify(self.destroot)
		geturl = module_url(urlroot, self.extension, self.pages)
		return {self.name: geturl}


class Rendered(Compiler, metaclass=abc.ABCMeta):
	"""Superclass for environment-rendering compilers."""
	def __init__(self, name, config):
		super().__init__(name, config)
		self.template = config.pop('template', self.name)
		self.context = config.pop('context', {})
		self.pages = {}
		for key in config.keys():
			raise Misconfigured('Unrecognized setting: %s' % key)

	def initialize(self, view):
		super().initialize(view)
		self.pages[view.url] = dict(self.context)

	@abc.abstractmethod
	def compile(self, view):
		super().compile(view)
		if view.url not in self.pages:
			self.initialize(view)

	def filters(self):
		urlroot = mite.util.path.urlify(self.destroot)
		geturl = module_context(urlroot, self.extension, self.pages)
		return {self.name: geturl}

	def remove(self, view):
		super().remove(view)
		view.reload(view.url)
