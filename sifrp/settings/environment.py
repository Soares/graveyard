from os.path import split, dirname, abspath
import socket
import server

# Project Description
PROJECT_NAME = 'sifrp'
PROJECT_ROOT = split(dirname(abspath(__file__)))[0]

# Miscelaneous Django Settings
ROOT_URLCONF = PROJECT_NAME + '.urls'
DEFAULT_FROM_EMAIL = 'webmaster@sifrp.com'
ADMINS = (('Nathaniel Soares', 'nate@natesoares.com'),)
MANAGERS = ADMINS
USE_I18N = True
INTERNAL_IPS = ('127.0.0.1',)
# mediagenerator makes etags uneccessary
USE_ETAGS = False

# Server Registration
server.register('AegonV', server.DEVELOPMENT, 'America/New_York', 'en-us')

# Server Selection
active = server.select(socket.gethostname())
TIME_ZONE = active.TIME_ZONE
LANGUAGE_CODE = active.LANGUAGE_CODE
DEBUG = active.TYPE == server.DEVELOPMENT

# Type Specific Settings
if DEBUG:
    CACHE_BACKEND = 'dummy:///'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    CACHE_BACKEND = 'dummy:///'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
