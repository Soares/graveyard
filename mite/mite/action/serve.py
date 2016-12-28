"""Mite local server."""
import http.server
import logging
import random
import signal
import socket
import socketserver
import threading

import mite.action.base
import mite.util.path


KEYWORD = 'serve'


class Action(mite.action.base.Action):
	"""Serve mite site on localhost."""

	def flagparser(self, *args, **kwargs):
		parser = super().flagparser(*args, **kwargs)
		mite.action.base.add_port_flag(
				parser, 'Run the local server on this port.')
		mite.action.base.add_debug_flag(parser)
		return parser

	def execute(self):
		super().execute()
		crawler = mite.action.base.crawler(self.config, self.port)
		serve(
			self.config.builddir,
			'localhost',
			self.port,
			crawler,
			self.config.delay)


def file_system_handler(directory):
	"""
	Creates a SimpleHTTPRequestHandler that serves out of a sub directory of
	the current directory.
	"""
	root = mite.util.path.urlify(directory)
	class FileSystemHandler(http.server.SimpleHTTPRequestHandler):
		def translate_path(self, path):
			assert path.startswith('/')
			return super().translate_path(root + path)

		def log_message(self, format, *args):
			logging.debug('%s - - [%s] %s',
					self.address_string(),
					self.log_date_time_string(),
					format % args)
	return FileSystemHandler


def runserver(server):
	thread = threading.Thread(target=server.serve_forever)
	thread.start()
	return thread


def serve(directory, host, port, crawler, delay):
	"""Runs a local server in directory, on port."""
	logging.info('Running webserver at http://localhost:%s', port)
	logging.info('Type control-c to exit')
	handler = file_system_handler(directory)
	httpd = socketserver.TCPServer(
			(host, port), handler, bind_and_activate=False)
	httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		httpd.server_bind()
		httpd.server_activate()
	except socket.error as error:
		raise mite.NotCurrentlyPossible(error)
	server_thread = runserver(httpd)
	try:
		crawler.watch(delay)
	except (KeyboardInterrupt, SystemExit):
		logging.info('Saving build & shutting down.')
		try:
			crawler.stop()
			httpd.shutdown()
			server_thread.join()
		except KeyboardInterrupt:
			logging.warning('Almost done!')
			logging.warning("If you hit CTRL-C again we'll stop immediately.")
			logging.warning('This will invalidate the build cache.')
			logging.warning('Startup may take longer next time.')
	if not random.randint(0, 12):
		# Spoilers ahead.
		logging.info('\n' + random.choice([
			'Fare well, fellow traveller.',
			'Never stop breathing.',
			'Nothing is impossible.',
			'Question everything.',
			'Strive for perfection.',
			'Live for beauty.',
			'Always Be Curious.',
			'You are valuable.']))
