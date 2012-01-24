#!/usr/bin/python

from distutils.core import setup

setup(
    name='CMDjango',
    version='0.1.0',
		description='CMDjango: On-the-fly CM compilation for Django',
    author='Nathaniel Soares',
    author_email='nate@natesoares.com',
		packages=['cmdjango', 'cmdjango.template', 'cmdjango.management', 'cmdjango.management.commands'],
)
