"""Built-in mite jinja filters."""
import logging
import os
import pprint

from mite import color


def module_url(root, extension, urls):
	"""
	Creates a url filter that gets the absolute url from a module-relative url.
	The urls set should contain the site-relative (final) urls.
	Example:

	{{ "some/path"|mymodule }}

	might expand to

	{{ nested/path/to/mymodule/some/path.html }}

	The url will be guessed and a logging.WARN issued if the url does note xist
	in the urls set. Leading slashes on the input argument are ignored.

	Flow has a special syntax for this filter: @module/some/path
	"""
	# It's really just a restricted module_context.
	# Don't tell anyone.
	context_filter = module_context(root, extension, urls)
	def url_filter(url, *args):
		return context_filter(url)
	return url_filter


def module_context(root, extension, urls):
	"""
	Creates a filter to get either a url or a page context item attached to
	that url. It's similar to module_url, except you may do things like:

	{{ "some/path"|mymodule("title") }}

	To get the "title" context item of the page at "some/path" relative to
	"mymodule".

	The 'urls' set should be site-relative urls. The user-given urls will be
	module-relative. The user-given url may ommit the extension so long as it
	matches 'extension'. It is recommended that you give a mutatable collection
	so that you may add/remove urls dynamically. Do not given an iterable, it
	will be expended on the first use.

	'root' should be the site-relative base url shared by every element of urls.

	A logging.WARN will be issued if the url does not exist. If the attribute
	is left blank or the url cannot be found, the url will be returned. If the
	attribute cannot be found on the item, None will be returned.

	Flow has a special syntax for this filter: @module.attribute/some/path
	"""
	root = root.rstrip('/') + '/'
	def context_filter(url, attribute=None):
		"""The jinja filter."""
		assert all(url.startswith(root) for url in urls), 'False root'
		url = root + url.lstrip('/')
		if extension is not None:
			url, ext = os.path.splitext(url)
			url += ext or extension
		if url not in urls:
			logging.warning(color.color('STUB: %s' % url, color.RED))
			return None if attribute else url
		if attribute is None:
			return url
		# Check the attribute first and the index second.
		return getattr(urls[url], attribute, urls[url].get(attribute, None))
	return context_filter
