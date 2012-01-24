import logging
from .setup import root
from . import conf

def render(strings):
	return ' '.join(map(str, strings))

class Logger:
	def __init__(self, name):
		self.logger = logging.getLogger(name)

	def log(self, level, *strings):
		self.logger.log(level, render(strings))

	def debug(self, *strings):
		self.logger.debug(render(strings))

	def info(self, *strings):
		self.logger.info(render(strings))

	def warning(self, *strings):
		self.logger.warning(render(strings))

	def error(self, *strings):
		self.logger.error(render(strings))

	def critical(self, *strings):
		self.logger.critical(render(strings))

logger = Logger('vee')

if conf.DEBUG:
	__builtins__['debug'] = logger.debug
