from django.core.management.base import BaseCommand
from sassdjango.management.settings import processors
from django import conf
import os
import re

def expander(property, process):
	regex = re.compile(r'\b(%s):(\s*)([^;]+);' % property)
	sub = lambda match: '\n'.join(process(match))
	return lambda file: regex.sub(sub, file)


class Command(BaseCommand):
	help = 'Post Process CSS files to help reduce tedium'

	def __init__(self, *args, **kwargs):
		super(Command, self).__init__(*args, **kwargs)
		self.expanders = [expander(p, r) for (p, r) in processors.items()]

	def process_dir(self):
		SASS_DEST = conf.settings.SASS_DEST
		print 'Processing directory %s...' % SASS_DEST
		for dirname, dirnames, filenames in os.walk(SASS_DEST):
			for filename in filter(lambda f: f.endswith('.css'), filenames):
				name = os.path.join(dirname, filename)
				with open(name) as infile:
					print "Processing %s..." % name
					output = self.process(infile.read())
				with open(name, 'w') as outfile:
					outfile.write(output)

	def process(self, string):
		return reduce(lambda f, e: e(f), self.expanders, string)

	def handle(self, *args, **kwargs):
		if len(args) == 0:
			return self.process_dir()
		if len(args) != 1:
			print 'One file at a time, please.'
			return
		filename, = args
		print 'Processing %s...' % filename
		with open(filename) as file:
			output = self.process(file.read())
		print output
