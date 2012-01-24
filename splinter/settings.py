from local.settings import *

PROJNAME = 'splinter'

ADMINS = ('Nate', 'nate@natesoares.com'),
MANAGERS = ADMINS
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
ROOT_URLCONF = PROJNAME + '.urls'
 

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'contact@natesoares.com'
EMAIL_HOST_PASSWORD = 'the heart asks pleasure first'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SENDER = 'contact@natesoares.com'


MEDIA_ROOT = ROOT + PROJNAME + MEDIA_URL
IMAGE_BASE = MEDIA_URL + 'css/images/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
PAGINATION = 20
DEFAULT_SENDER = EMAIL_SENDER
 

SASS_DIR = MEDIA_ROOT + 'sass/'
CSS_DIR = MEDIA_ROOT + 'css/'
CM_DIR = ROOT + PROJNAME + '/templates/cm/'
HTML_DIR = ROOT + PROJNAME + '/templates/compiled/'


TEMPLATE_LOADERS += (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
 
TEMPLATE_DIRS = (
    ROOT + PROJNAME + '/templates/compiled',
    ROOT + PROJNAME + '/templates/finished',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.csrf',
)
 
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
)
 
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.markup',
    'django.contrib.sites',
    'django.contrib.webdesign',
	'django.contrib.comments',

    'south',
	'sassdjango',
	'cmdjango',
	'utilities',
	'splinter.entries',
)
