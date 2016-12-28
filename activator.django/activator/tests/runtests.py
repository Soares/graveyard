#!/usr/bin/env python
import os, sys
from django.conf import settings

DIRNAME = os.path.dirname(__file__)
settings.configure(DEBUG = True,
                   DATABASE_ENGINE = 'sqlite3',
                   DATABASE_NAME = os.path.join(DIRNAME, 'database.db'),
                   ROOT_URLCONF = 'activator.urls',
                   ACTIVATOR_USER_MODEL = 'mockapp.User',
                   AUTHENTICATION_BACKENDS = ('activator.backends.TokenBackend',),
                   TEMPLATE_DIRS = ('activator/tests/mockapp/templates',),
                   INSTALLED_APPS = ('django.contrib.auth',
                                     'django.contrib.contenttypes',
                                     'django.contrib.sessions',
                                     'django.contrib.admin',
                                     'activator.tests.mockapp',
                                     'activator.tests',
                                     'activator',))


from django.test.simple import run_tests

failures = run_tests(['activator',], verbosity=1)
if failures:
    sys.exit(failures)
