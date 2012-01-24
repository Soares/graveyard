from django.core.management.base import BaseCommand
from django.conf import settings
from cmdjango import converter
import os
import re


class Command(BaseCommand):
    help = 'Run CM to generate HTML files'
    auto_convert = re.compile(r'^[^_].*\.cm$')

    def handle(self, *filenames, **kwargs):
        if filenames:
            for filename in filenames:
                if filename.endswith('.txt'):
                    filename = filename[:-4]
                if filename.endswith('.html'):
                    filename = filename[:-5]
                print converter.convert(filename)
            return

        front = len(settings.CM_IN_DIR)
        for dirname, dirnames, filenames in os.walk(settings.CM_IN_DIR):
            dir = dirname[front:]
            for filename in filter(self.auto_convert.match, filenames):
                self.handle(os.path.join(dir, filename))
