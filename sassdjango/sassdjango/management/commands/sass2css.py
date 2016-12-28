from django.core.management.base import BaseCommand
from django import conf
from subprocess import Popen, PIPE
from optparse import make_option
import os
import re

candidate = re.compile(r'^[^_].*\.sass$')


class Command(BaseCommand):
	help = """Convert SASS files to CSS files."""
	option_list = BaseCommand.option_list + (
		make_option('-r', '--raw',
			action='store_true', dest='raw', default=False,
			help="don't post-process the file with 'procss'"),)

	def destination(self, sassfile):
		SASS_DIR = conf.settings.SASS_DIR
		SASS_DEST = conf.settings.SASS_DEST
		assert sassfile.startswith(SASS_DIR)
		assert sassfile.endswith('.sass')
		relative = sassfile[len(SASS_DIR):-len('.sass')]
		return SASS_DEST + relative + '.css'

	def convert_dir(self, raw=False):
		from sassdjango.management.commands.procss import Command as Procss
		process = Procss().process
		SASS_DIR = conf.settings.SASS_DIR
		for dirname, dirnames, filenames in os.walk(SASS_DIR):
			for filename in filter(candidate.match, filenames):
				name = os.path.join(dirname, filename)
				print '\tReading %s...' % name
				with open(name) as infile:
					output, err = self.convert(infile.read())
				dest = self.destination(name)
				if err:
					print '\tErrors in %s: %s' % (filename, err)
					continue
				if not raw:
					print '\tPostprocessing %s...' % name
					output = process(output)
				print '\tWriting %s...' % dest
				with open(dest, 'w') as outfile:
					outfile.write(output)

	def convert(self, string):
		SASS_EXE = conf.settings.SASS_EXE
		proc = Popen((SASS_EXE, '-s'), stdin=PIPE, stdout=PIPE)
		return proc.communicate(input=string)

	def handle(self, *args, **kwargs):
		SASS_DIR = conf.settings.SASS_DIR
		if len(args) == 0:
			print 'Converting directory %s...' % SASS_DIR
			return self.convert_dir(raw=kwargs.get('raw'))
		if len(args) != 1:
			print 'One file at a time, please.'
			return
		filename, = args
		print 'Processing %s...' % filename
		with open(filename) as file:
			output = self.convert(file.read())
		print output
