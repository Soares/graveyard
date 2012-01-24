#!/usr/bin/env python
from distutils.command.config import config
from distutils.core import setup

class Config(config):
    description = 'Configure cm'
    user_options = [('sass=', 's', 'location of sass executable')]
    sass = None
    def run(self, *args, **kwargs):
        import os
        file = open(os.path.join('cm', 'config.py'), 'w')
        if self.sass:
            self.sass = os.path.expanduser(os.path.expandvars(self.sass))
            self.sass = "'%s'" % self.sass
        file.write('sass = %s' % self.sass)
        file.close()

setup(
    name='CM',
    version='0.9a',
    description='Concise Markup: An HTML compiler and template language',
    author='Nate Soares',
    author_email='nate@natesoares.com',
    # url='http://cm.natesoares.com',
    packages=[
        'cm', 'cm.functions', 'cm.nodes', 'cm.utilities',
        'cm.lexer', 'cm.lexer.output', 'cm.parser', 'cm.parser.output',
    ],
    cmdclass={'config': Config},
)
