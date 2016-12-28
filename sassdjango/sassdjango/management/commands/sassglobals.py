from django.core.management.base import BaseCommand
from sassdjango.management.settings import settings
from optparse import make_option
from django import conf
import os

class Command(BaseCommand):
	help = 'Generate a sass "settings" file containing django config settings'
	option_list = BaseCommand.option_list + (
		make_option('-f', '--filename',
			dest='filename', metavar='FILE',
			help='write output to FILE (in SASS_DIR unless -r is given)'),
		make_option('-r', '--relative',
			action="store_true", dest="relative", default=False,
			help="output to FILE relative to here, not SASS_DIR"))

	def handle(self, *args, **kwargs):
		output = '\n'.join('$%s: %s' % (k, getattr(conf.settings, v))
				for (k, v) in settings.items())
		filename = kwargs.get('filename', False)
		if not filename:
			print output
			return
		if not kwargs.get('relative'):
			SASS_DIR = conf.settings.get('SASS_DIR')
			filename = os.path.join(SASS_DIR, filename)
		print 'Writing to %s...' % filename
		with open(filename, 'w') as file:
			file.write(output)
