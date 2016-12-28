"""Trivial copying compiler."""
import shutil
import logging

from mite.compiler.base import Contained


class Copier(Contained):
	"""Copies files from source to destination."""

	def compile(self, view):
		logging.info('Copying %s', view.url)
		shutil.copyfile(view.source, view.destination)
