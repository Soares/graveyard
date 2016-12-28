"""Template 'compilers' (read: dependency managers)."""
import logging

from mite.compiler.base import Compiler
from mite.compiler.jinja import dependencies

class Template(Compiler):
	def __init__(self):
		super().__init__('<templates>', {})

	def initialize(self, view):
		pass  # super() makes directories in .build/

	def remove(self, view):
		pass  # We don't actually compile anything.

	def compile(self, view):
		for n in map(view.neighbor, dependencies(view.read(), view.url)):
			logging.debug('%s depends on %s', view.url, n.url)
			view.depend(n.source)
