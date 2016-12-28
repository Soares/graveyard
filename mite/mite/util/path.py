"""Mite path functions."""
import os


def urlify(filepath):
	"""
	Turns a filepath into an absolute url.

	>>> urlify('/foo/bar.html')
	'/foo/bar.html'
	>>> urlify('foo/./bar.html')
	'/foo/bar.html'

	"""
	return '/' + '/'.join(components(filepath))


def components(path):
	"""
	Completely split a path into components.
	You'll know longer be able to tell if it was absolute or relative.

	>>> components('/foo/bar/baz')
	['foo', 'bar', 'baz']
	>>> components('/foo/./bar/baz')
	['foo', 'bar', 'baz']
	>>> components('/foo')
	['foo']
	>>> components('.')
	[]
	>>> components('/')
	[]
	>>> components('')
	[]

	"""
	# Necessary because normpath('') is '.'
	if path in ('', '.'):
		return []
	rest, last = os.path.split(os.path.normpath(path))
	# not last implies we've hit the bottom of an absolute path.
	# not rest implies we've hit the bottom of a relative path.
	return ((components(rest) if rest else []) + [last]) if last else []


def directory(path):
	"""
	Gets the first path component in a path.

	>>> directory('foo/bar/baz')
	'foo'
	>>> directory('foo')
	'foo'

	"""
	return components(path)[0]
