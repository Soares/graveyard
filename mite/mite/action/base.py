"""
The mite action interace.
All Mite modules should have an Action subclass named Action
and a string keyword named KEYWORD.
"""
import abc
import argparse
import itertools
import jinja2
import logging
import os
import pprint
import yaml

import mite.config
import mite.refresher
import mite.sourcetree
import mite.compiler.template


DEFAULT_PORT = 1025


def crawler(config, port=None):
	"""Creates a sourcetree crawler."""
	os.makedirs(config.builddir, exist_ok=True)
	os.makedirs(config.cachedir, exist_ok=True)
	filters = dict(itertools.chain(
			*(c.filters().items() for c in config.compilers)))
	logging.debug('Template filters: %s', pprint.pformat(list(filters)))
	config.globals.update(dict(itertools.chain(
			*(c.globals().items() for c in config.compilers))))
	logging.debug('Template globals: %s', pprint.pformat(config.globals))
	refresh = mite.refresher.Refresher(
			port=port) if port else mite.refresher.Dummy()
	environment = jinja2.Environment(
			extensions=['jinja2.ext.do'],
			loader=jinja2.ChoiceLoader(
				[jinja2.FileSystemLoader(config.templatedir)] + list(
					itertools.chain(*(c.loaders()
						for c in config.compilers)))))
	environment.globals.update(config.globals)
	environment.filters.update(filters)
	crawler = mite.sourcetree.crawler.Crawler(
			builddir=config.builddir,
			cachedir=config.cachedir,
			templatedir=config.templatedir,
			environment=environment,
			refresher=refresh,
			lag=config.lag)
	# Enables dependency checking on the template directory.
	crawler.register(config.templatedir, mite.compiler.template.Template())
	for compiler in config.compilers:
		logging.debug('Registering module %s', compiler.name)
		crawler.register(compiler.name, compiler)
	return crawler


class Action(metaclass=abc.ABCMeta):
	"""
	Common action framework.
	Actions are welcome to not extend this action so long as they implement
	__init__(self, flags) and execute(self).
	"""

	debug = False

	def __init__(self, prog, keyword, *flags):
		self.prog = prog
		self.flagparser(prog, keyword).parse_args(flags, namespace=self)
		loglevel = logging.DEBUG if self.debug else logging.INFO
		logging.basicConfig(format='%(message)s', level=loglevel)
		if not os.path.exists(self.site):
			raise mite.Misconfigured("Can't find {}".format(self.site))
		if os.path.isdir(self.site):
			self.config_filename = mite.config.Config.FILENAME
		else:
			assert os.path.isfile(self.site)
			self.site, self.config_filename = os.path.split(self.site)

	def flagparser(self, prog, keyword):
		"""An ArgumentParser to parse the flags."""
		parser = argparse.ArgumentParser(prog='{} {}'.format(prog, keyword))
		add_site_flag(parser)
		return parser

	def configure(self):
		"""
		Reads and returns the site configuration.
		Must be done from within the site directory.
		"""
		try:
			with open(self.config_filename) as configfile:
				data = yaml.load(configfile)
		except PermissionError:
			raise mite.Misconfigured(
				"{} doesn't have permission to read {}".format(
					self.prog, self.config_filename))
		except yaml.error.YAMLError as error:
			raise mite.Misconfigured(
				'Invalid syntax in config file:\n\n'.format(error))
		return mite.config.Config(data)

	def enter(self):
		"""Enters the site directory."""
		assert os.path.isdir(self.site)
		try:
			os.chdir(self.site)
		except PermissionError:
			raise mite.Misconfigured(
				"{} doesn't have permission to enter {}".format(
					self.prog, self.site))
		if not os.path.isfile(self.config_filename):
			raise mite.Misconfigured(
				'{} is not a readable file.'.format(self.config_filename))

	@abc.abstractmethod
	def execute(self):
		"""Executes the action."""
		self.enter()
		self.config = self.configure()


def add_site_flag(parser):
	"""Adds the positional site flag to the parser."""
	parser.add_argument(
			'site',
			nargs='?',
			metavar='SITE',
			default=os.getcwd(),
			help="""
			The directory containing the site.
			May also point to a yaml file in the root directory of the site.
			Default: current directory.
			""")


def add_port_flag(parser, message):
	"""Adds the optional port flag to the parser."""
	message += 'Default: {}.'.format(DEFAULT_PORT)
	parser.add_argument(
			'--port', '-p',
			const=DEFAULT_PORT,
			default=DEFAULT_PORT,
			metavar='PORT',
			nargs='?',
			type=int,
			help=message)
	return parser


def add_debug_flag(parser, message='Print lots of logs.'):
	"""Adds the standard debug flag to an argument parser."""
	parser.add_argument(
			'--debug',
			action='store_true',
			default=False,
			help=message)
	return parser
