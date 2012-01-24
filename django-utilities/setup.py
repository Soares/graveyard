#!/usr/bin/python

from distutils.core import setup

setup(
    name='DjangoUtilities',
    version='0.1.0',
	description='Django Utilities ',
    author='Nathaniel Soares',
    author_email='nate@natesoares.com',
	packages=['utilities', 'utilities.forms', 'utilities.models', 'utilities.templatetags', 'utilities.views'],
)
