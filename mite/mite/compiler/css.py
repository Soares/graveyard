"""Base CSS compiler."""
import abc

from mite.compiler.base import Compiler


class CSS(Compiler, metaclass=abc.ABCMeta):
	"""Superclass for css compilers."""

	extension = '.css'

	@abc.abstractmethod
	def compile(self, view):
		super().compile(view)
		view.restyle()

