"""Mite browser manipulation. Does autoreloading when serving locally."""
import logging
import platform
import subprocess
import threading
import time
from urllib.parse import urljoin, urlparse

# Used to differentiate between refresh actions.
# The values must be different, but are only used for logging.
RELOAD = 'reload'
RESTYLE = 'restyle'


class Refresher:
	"""An object that runs javascript on any browser tabs viewing the site."""
	def __init__(self, host='localhost', port=1025):
		self.url = 'http://{host}:{port}'.format(host=host, port=port)
		self.reset()

	def reload(self, url=None):
		self.reloading.add(url)

	def restyle(self, url=None):
		self.restyling.add(url)

	def reset(self):
		self.reloading = set()
		self.restyling = set()

	def execute(self):
		if None in self.reloading or len(self.reloading) > 3:
			execute(RELOAD, self.url)
			# We've fully refreshed everything.
			# No need to traverse individual URLs to refresh/restyle them.
			self.reset()
			return
		for url in self.reloading:
			execute(RELOAD, self.url, url)
			self.restyling.discard(url)
		if None in self.restyling or len(self.restyling) > 3:
			execute(RESTYLE, self.url)
			# We refreshed everything.
			# No need to restyle individual URLs again.
			self.reset()
			return
		for url in self.restyling:
			execute(RESTYLE, self.url, url)
		self.reset()


class Dummy(Refresher):
	"""An object that looks like a Refresher but doesn't do anything."""
	def execute(self):
		self.reset()


def execute(command, root, url=None):
	# TODO: Support more platforms.
	if platform.system() == 'Darwin':
		mac_do(command, root, url)


def mac_do(command, root, url=None):
	"""Tell the browser to refresh on macs."""
	psdata = subprocess.check_output(['ps', 'aux']).decode('utf-8')
	if url is None:
		query = 'starts with "%s"' % root
	elif url in ('/index.html', 'index.html'):
		query = 'is "%s" or thisTab\'s url starts with "%s"' % (
				root.rstrip('/') + '/', urljoin(root, url))
	else:
		query = 'starts with "%s"' % urljoin(root, url)
	for app, scripts in MAC_SCRIPTS.items():
		if app in psdata:
			assert command in scripts
			script = scripts[command].format(
					application=app,
					query=query)
			logging.debug('Running apple script:\n%s', script)
			applescript = 'osascript<<END{0}END'.format(script)
			action = url or 'ALL'
			logging.info('Sending %s %s signal to %s', command, action, app)
			subprocess.Popen(applescript, shell=True)


# We must avoid newlines. (Applescript doesn't support them easily.)
# We must avoid double quotes. (This will be embedded in quotes in Applescript.)
# We must avoid curly braces. (This will be formatted with .format in python.)
JAVASCRIPT_RELOAD_LINKS = (
	"var links = document.getElementsByTagName('link');"
	"for(var i = 0; i < links.length; i++)"
		"if(links[i].rel == 'stylesheet')"
			"links[i].href += '';")


MAC_BROWSER_TABDO = """
tell application "{application}"
	repeat with thisWindow in every window
		repeat with thisTab in thisWindow's tabs
			if thisTab's url {query}
				%s
			end if
		end repeat
	end repeat
end tell
"""
MAC_COMMAND_RESTYLE_CHROME = (
	'execute thisTab javascript "%s"' % JAVASCRIPT_RELOAD_LINKS)
MAC_COMMAND_RESTYLE_SAFARI = (
	'tell thisTab to do JavaScript "%s"' % JAVASCRIPT_RELOAD_LINKS)
MAC_SCRIPTS = {
	'Google Chrome': {
		RELOAD: MAC_BROWSER_TABDO % 'reload thisTab',
		RESTYLE: MAC_BROWSER_TABDO % MAC_COMMAND_RESTYLE_CHROME,
	},
	'Safari': {
		RELOAD: MAC_BROWSER_TABDO % 'reload thisTab',
		RESTYLE: MAC_BROWSER_TABDO % MAC_COMMAND_RESTYLE_SAFARI,
	},
}
