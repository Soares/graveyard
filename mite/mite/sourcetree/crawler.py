"""Reacting to mite site changes."""
from datetime import datetime, timedelta
from collections import defaultdict
import itertools
import logging
import os
import pickle
import subprocess
import sys
import time
import traceback

from mite import Misconfigured
from mite import util
from mite.sourcetree import views
from mite.sourcetree import dependencies
from mite.sourcetree import tree

BUILDSTATE_FILE = 'build'
SOURCETREE_FILE = 'sourcetree'
DEPENDENCY_FILE = 'dependencies'


class Crawler:
	def __init__(self,
			builddir,
			cachedir,
			templatedir,
			environment,
			refresher,
			lag):
		assert os.path.isdir(builddir)
		assert os.path.isdir(cachedir)
		assert os.path.isdir(templatedir)

		self.builddir = builddir
		self.templatedir = templatedir
		self.env = environment
		self.refresher = refresher
		self.lag = lag

		self.buildstate_filename = os.path.join(cachedir, BUILDSTATE_FILE)
		self.sourcetree_filename = os.path.join(cachedir, SOURCETREE_FILE)
		self.dependency_filename = os.path.join(cachedir, DEPENDENCY_FILE)
		self.load_state()

		self.watching = {}
		self.processes = set()

	def register(self, directory, manager):
		"""Watch a directory with a manager."""
		if directory in self.watching:
			raise Misconfigured('{} and {} both want to compile {}'.format(
				self.watching[directory], manager, directory))
		self.watching[directory] = manager
		# A "none" manager means that the directory is not compiled, but may be
		# depended upon. (For example, the template directory.)
		if manager is None:
			return
		for (dirpath, _, filenames) in os.walk(directory):
			for filename in filenames:
				filepath = os.path.join(dirpath, filename)
				manager.initialize(self.init_view(manager, directory, filepath))

	def updates(self):
		removed, changed = util.either.sets(itertools.chain(
			*(self.sourcetree[d].walk(d) for d in self.watching)))
		for path in removed:
			del self.dependencies[path]
		for path in set(changed):
			changed.update(self.dependencies[path])
		return removed, changed

	def update(self, removed, changed):
		"""Notify managers when files have changed."""
		self.processes.clear()
		for path in removed:
			directory = util.path.directory(path)
			manager = self.watching.get(directory)
			if manager:  # 'None' is a dummy watcher.
				manager.remove(self.remove_view(manager, directory, path))
		for path in changed:
			directory = util.path.directory(path)
			del self.dependencies[path]  # Dependencies get stale.
			manager = self.watching.get(directory)
			if manager:  # 'None' is a dummy watcher.
				manager.compile(self.compile_view(manager, directory, path))
		while self.processes:
			self.processes.pop().wait()
		self.save_state()
		time.sleep(self.lag)
		self.refresher.execute()

	def build(self):
		"""Builds the site once."""
		logging.debug('Building %s', self.builddir)
		self.update(*self.updates())

	def watch(self, delay):
		"""Starts watching the source tree."""
		while True:
			try:
				removed, changed = self.updates()
				if changed or removed:
					self.update(removed, changed)
				else:
					time.sleep(delay)
			except Exception as e:
				logging.error('#' * 80)
				logging.error('# ERROR')
				logging.error('#')
				logging.debug(''.join(traceback.format_exception(
					*sys.exc_info())))
				logging.error(repr(e))
				logging.error('Press enter when the error is fixed.')
				try:
					input('> ')
				except EOFError:
					raise SystemExit

	def stop(self):
		"""Stops the watching (at the end of the next cycle)."""
		if self.processes:
			logging.debug('Killing all running processes.')
		for process in self.processes:
			logging.debug('Murdering %s', process)
			process.kill()

	def load_state(self):
		"""
		Loads saved state from the cache files if possible.
		Initializes savable state to the defaults otherwise.
		"""
		last_build = read_cachefile(self.buildstate_filename)
		if os.path.getmtime(self.builddir) == last_build:
			logging.info("Build directory hasn't changed since last time.")
			logging.info("I'll reuse it.")
			self.sourcetree = read_cachefile(self.sourcetree_filename)
			self.dependencies = read_cachefile(self.dependency_filename)
		else:
			logging.debug('Build cache has been invalidated.')
			logging.debug('Rebuilding from scratch.')
			self.sourcetree, self.dependencies = None, None
		self.sourcetree = self.sourcetree or defaultdict(tree.Tree)
		self.dependencies = self.dependencies or dependencies.Graph()

	def save_state(self):
		"""Saves current state to the cache files."""
		for tree in self.sourcetree.values():
			tree.commit()
		lastbuild = os.path.getmtime(self.builddir)
		write_cachefile(self.buildstate_filename, lastbuild)
		write_cachefile(self.sourcetree_filename, self.sourcetree)
		write_cachefile(self.dependency_filename, self.dependencies)

	def init_view(self, module, directory, path):
		"""Available during file initialization."""
		return views.Initializing(
				sourcepath=path,
				sourceroot=directory,
				builddir=self.builddir,
				destroot=module.destroot,
				extension=module.extension)

	def remove_view(self, module, directory, path):
		"""Available during file removal."""
		return views.Removing(
				sourcepath=path,
				sourceroot=directory,
				builddir=self.builddir,
				destroot=module.destroot,
				refresher=self.refresher,
				processes=self.processes,
				extension=module.extension)

	def compile_view(self, module, directory, path):
		"""Available during file compilation."""
		return views.Compiling(
				env=self.env,
				sourcepath=path,
				sourceroot=directory,
				modules=self.watching,
				builddir=self.builddir,
				destroot=module.destroot,
				refresher=self.refresher,
				processes=self.processes,
				templatedir=self.templatedir,
				extension=module.extension,
				dependencies=self.dependencies)


def read_cachefile(filename):
	if not os.path.exists(filename):
		return None
	with open(filename, 'rb') as filehandle:
		try:
			data = pickle.load(filehandle)
		except (pickle.UnpicklingError, EOFError):
			logging.warning('Bad cache: %s', filename)
			return None
	return data


def write_cachefile(filename, data):
	with open(filename, 'wb') as filehandle:
		pickle.dump(data, filehandle)
