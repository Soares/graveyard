"""Cleans the site."""
import logging
import shutil

import mite.action.base
import mite.util.input


KEYWORD = 'clean'


class Action(mite.action.base.Action):
	"""Remove up the compiled site."""

	def flagparser(self, *args, **kwargs):
		parser = super().flagparser(*args, **kwargs)
		parser.add_argument(
				'--force', '-f',
				action='store_true',
				default=False,
				help='Skip confirmation.')
		return parser

	def execute(self):
		super().execute()
		if self.force or mite.util.input.confirm(
				'Clear the built site?', default=True):
			shutil.rmtree(self.config.builddir, True)
			shutil.rmtree(self.config.cachedir, True)
			logging.info('Cleaned.')
