#!/usr/bin/python

from distutils.core import setup

setup(
    name='SassDjango',
    version='0.1.0',
		description='SassDjango: On-the-fly SASS compilation for Django',
    author='Nathaniel Soares',
    author_email='nate@natesoares.com',
		packages=['sassdjango', 'sassdjango.management', 'sassdjango.management.commands'],
)
