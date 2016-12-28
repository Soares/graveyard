"""Base javascipt compiler."""
import abc

from mite.compiler.base import Compiler


class Javascript(Compiler, metaclass=abc.ABCMeta):
	"""Superclass for js compilers."""
	extension = '.js'

	@abc.abstractmethod
	def compile(self, view):
		super().compile(view)
		view.reload()
