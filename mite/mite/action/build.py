"""Builds the site."""
import mite.action.base


KEYWORD = 'build'


class Action(mite.action.base.Action):
	"""Build mite site."""

	def flagparser(self, *args, **kwargs):
		parser = super().flagparser(*args, **kwargs)
		mite.action.base.add_port_flag(parser, """
				The port that web browsers are viewing this site on.
				If you're on a macintosh, they will be refreshed.
				To disable auto-refreshing use port 0.
				""")
		mite.action.base.add_debug_flag(parser)
		return parser

	def execute(self):
		super().execute()
		mite.action.base.crawler(self.config).build()
