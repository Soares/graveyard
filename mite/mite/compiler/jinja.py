"""Jinja mite compilers."""
import abc
import copy
import logging
import jinja2
import pprint
import re

from mite.compiler.base import Rendered


class Jinja(Rendered):
	"""Compiles vanilla jinja templates."""

	def loaders(self):
		return (jinja2.loaders.FileSystemLoader(self.buildpath),)

	def compile(self, view):
		super().compile(view)
		logging.info('Templating %s', view.url)
		view.write(view.render_template(view.source, self.pages[view.url]))
		for n in map(view.neighbor, dependencies(view.read(), view.url)):
			logging.debug('%s depends on %s', view.url, n.url)
			view.depend(n.source)
		view.reload(view.url)


class Dynamic(Rendered, metaclass=abc.ABCMeta):
	"""Compiles jinja templates from strings generated from files."""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__contents = {}

	def initialize(self, view):
		super().initialize(view)
		self.update(view)

	def update(self, view):
		"""
		Updates the globally-available context of a page.
		(post1 needs to be able to access post2.title before post2 has been
		rendered.) Also caches the page contents.
		"""
		text = view.read()
		content, context = self.parse(text, copy.deepcopy(self.context))
		self.__contents[view.url] = content
		self.pages[view.url] = context

	def compile(self, view):
		super().compile(view)
		self.update(view)
		context = self.pages[view.url]
		if not self.publish(context):
			logging.info('Skipping %s (unpublished)', view.url)
		logging.info('Writing %s', view.url)
		content = self.template_string(self.__contents[view.url], context, view)
		logging.debug('==== RENDERING ===================================')
		logging.debug(content)
		logging.debug('==== WITH CONTEXT ================================')
		logging.debug(pprint.pformat(context))
		logging.debug('==================================================')
		view.write(view.render(content, context))
		view.reload(view.url)

	@abc.abstractmethod
	def parse(self, text):
		"""Return (content, context) from the page text."""

	@abc.abstractmethod
	def template_string(self, text, context):
		"""Generates a jinja template from the text and context."""

	def publish(self, context):
		"""Chooses whether or not to publish the page given the page context."""
		return True


def dependencies(jinja, name=None):
	"""
	The dependencies in a jinja file.

	>>> list(dependencies('{% extends "foo.html" %}{% include "bar.html" %}'))
	['foo.html', 'bar.html']
	>>> DEPENDS_VARIABLE.match('{% extends "foo.html" %}')
	>>> DEPENDS_VARIABLE.match('{% extends foo %}') is not None
	True
	"""
	if DEPENDS_VARIABLE.match(jinja):
		who = ' ({})'.format(name) if name else ''
		logging.warning('Untrackable dependency!%s' % who)
		logging.warning('Template seems to extend/include a variable.')
	for _, filename in DEPENDS_STATEMENT.findall(jinja):
		yield filename



DEPENDS_STATEMENT = re.compile(
	r"""{%\s*(?:extends|include)\s*(['"])((?:[^\1\\\n%}]|\\.)*)\1\s*%}""")
DEPENDS_VARIABLE = re.compile(
	r"""{%\s*(?:extends|include)\s*[a-zA-Z_]""")
