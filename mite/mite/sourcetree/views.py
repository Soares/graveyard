"""
Limited actions and properties available to compilers during specific stages.
For example, the CompileView provides Executing, Refreshing, Reading, Depending,
etc. to compilers during the compilation step.
"""
import abc
import os
import subprocess

from mite import Misconfigured
import mite.util.path

class View(metaclass=abc.ABCMeta):
	"""A view type. All views should accept and pass along all init kwargs."""
	def __init__(self, **kwargs):
		pass


class FileKnowing(View):
	"""Gives access to different names for the same filepath."""

	def __init__(self, **kwargs):
		self.__sourceroot = kwargs['sourceroot']
		self.__destroot = kwargs['destroot']
		self.__builddir = kwargs['builddir']
		rel_path_ext = os.path.relpath(kwargs['sourcepath'], self.__sourceroot)
		self.__relpath, self.__sourcext = os.path.splitext(rel_path_ext)
		self.__destext = kwargs['extension']
		super().__init__(**kwargs)

	@property
	def sourcext(self):
		"""The input file's extension"""
		return self.__sourcext

	@property
	def destext(self):
		"""The extension that the output file should have"""
		return self.sourcext if self.__destext is None else self.__destext

	@property
	def source(self):
		"""The input path relative to the current directory."""
		return os.path.join(self.__sourceroot, self.__relpath) + self.sourcext

	@property
	def relpath(self):
		"""The path of the file (from the module directory)."""
		return self.__relpath + self.sourcext

	@property
	def destination(self):
		"""The build path relative to the current directory."""
		return os.path.normpath(os.path.join(
				self.__builddir,
				self.__destroot,
				self.__relpath + self.destext))

	@property
	def url(self):
		"""The url of the file (from the root of the site)."""
		return mite.util.path.urlify(os.path.join(
			self.__destroot, self.__relpath + self.destext))

	@property
	def relurl(self):
		"""The url of the file relative to the module."""
		return mite.util.path.urlify(self.__relpath + self.destext)

	def neighbor(self, path):
		"""
		The FileKnowing view of a neighboring path in the same module.
		'path' must be module-relative.
		"""
		return FileKnowing(
				builddir=self.__builddir,
				destroot=self.__destroot,
				extension=self.__destext,
				sourceroot=self.__sourceroot,
				sourcepath=os.path.join(self.__sourceroot, path))


class FileReading(FileKnowing):
	"""Gives access to a file handle."""

	def read(self):
		"""Reads the input file."""
		with open(self.source) as handle:
			return handle.read()


class FileHandling(FileReading):
	"""
	Gives access to a writable file handle.
	Makes it easier for us to test things.
	"""

	def write(self, data):
		"""Write the data to the output file."""
		with open(self.destination, 'w') as handle:
			handle.write(data)


class Dependable(View):
	"""Gives access to a dependency manager for files."""

	def __init__(self, **kwargs):
		self.__path = kwargs['sourcepath']
		self.__dependencies = kwargs['dependencies']
		super().__init__(**kwargs)

	def depend(self, *dependencies):
		"""
		Adds dependencies from the viewed file to other files.
		Dependency paths should be site-relative.
		"""
		self.__dependencies.update(self.__path, dependencies)


class Refreshing(View):
	"""Limited context and actions for refreshing a browser."""

	def __init__(self, **kwargs):
		self.__refresher = kwargs['refresher']
		super().__init__(**kwargs)

	def reload(self, url=None):
		self.__refresher.reload(url)

	def restyle(self, url=None):
		self.__refresher.restyle(url)


class Executing(View):
	"""Limited context and actions for firing and forgetting subprocesses."""

	def __init__(self, **kwargs):
		self.__processes = kwargs['processes']
		super().__init__(**kwargs)

	def execute(self, *args, **kwargs):
		self.__processes.add(subprocess.Popen(*args, **kwargs))


class Rendering(View):
	"""Limited context and actions for rendering jinja templates."""

	def __init__(self, **kwargs):
		self.__env = kwargs['env']
		self.__templatedir = kwargs['templatedir']
		super().__init__(**kwargs)

	@property
	def environment(self):
		"""Gets the jinja environment."""
		return self.__env

	def template_path(self, name):
		return os.path.join(self.__templatedir, name)

	def pick_template(self, *names):
		for template in names:
			path = self.template_path(template)
			if os.path.isfile(path):
				return os.path.relpath(path, self.__templatedir)
		raise Misconfigured('Missing Template(s): {}'.format(', '.join(names)))

	def render(self, content, context):
		"""Jinja-renders a content string with a context dictionary."""
		return self.__env.from_string(content).render(context)

	def render_template(self, template, context):
		"""Jinja-renders a template with a context."""
		return self.__env.get_template(template).render(context)


class SiblingAware(View):
	"""Limited context and actions for modules that know about other modules."""

	def __init__(self, **kwargs):
		self.__modules = kwargs['modules']
		super().__init__(**kwargs)

	@property
	def modules(self):
		"""Gets the names of all modules."""
		return set(self.__modules)


class Initializing(FileReading):
	"""The actions and properties available during file initialization."""


class Removing(FileKnowing, Refreshing, Executing):
	"""The actions and properties available during file removal."""


class Compiling(
		SiblingAware, Refreshing, Executing,
		Rendering, FileHandling, Dependable):
	"""The actions and properties available during file compilation."""
