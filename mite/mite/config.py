"""
Mite Site configuration. Config is the bastion protecting all other classes
from the insanity that is human input. Configs do all the icky magic and
guessing so that all of the other classes can have a clean interface.
"""

import imp
import logging
import os
import re
import yaml

from mite import Misconfigured
import mite.compiler.loader


COMPILETO = re.compile(r'([a-zA-Z_][a-zA-Z_0-9]*)\s+to\s+(.*)')


class Config:
	"""The site configuration."""

	FILENAME = 'config.yaml'
	DEFAULT_COMPILER = 'flow'

	def __init__(self, config):
		# Special config variable for site configuration.
		site = config.pop('site', {})
		# Special site directories.
		self.builddir = site.pop('build', '.build')
		self.cachedir = site.pop('cache', '.cache')
		self.templatedir = site.pop('templates', 'templates')
		compilerdir = site.pop('compilers', 'compilers')
		for directory in (self.templatedir, compilerdir):
			if not os.path.isdir(directory):
				raise Misconfigured('{} directory not found.'.format(directory))
		# Mite timing options.
		self.delay = site.pop('delay', 0.5)
		self.lag = site.pop('lag', 0.1)
		# Global module configuration.
		fallback = site.pop('compiler', self.DEFAULT_COMPILER)
		self.globals = site.pop('globals', {})
		# That's all the configuration options recognized in 'site'.
		for key in site:
			raise Misconfigured('Unrecognized site configuration: %s' % key)
		# All remaining configurations are modules.
		loader = mite.compiler.loader.Loader(fallback, compilerdir)
		self.compilers = [loader.load(m, module_config_dict(m, c))
				for m, c in config.items()]


def module_config_dict(name, config):
	"""
	Parses a configuration (bool/string/dict) into dict form.
	module: true gets {to: module}
	module: dir/ gets {to: dir/}
	module: COMPILER to LOCATION gets {'compiler': COMPILER, 'to': LOCATION}
	Dicts are passed through unmolested. Everything else is a Misconfigured.
	"""
	if config is True:
		return {'to': name}
	elif isinstance(config, str):
		match = COMPILETO.match(config)
		if match:
			compiler, to = match.groups()
			return {'compiler': compiler, 'to': to}
		return {'to': config}
	elif isinstance(config, dict):
		return config
	raise Misconfigured('Unusable configuration for %s: %s', name, config)
