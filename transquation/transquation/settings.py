import os.path
import socket
setting = lambda generator: tuple(generator())
path = lambda *args: os.path.normpath(os.path.realpath(os.path.join(*args)))

# SETUP {{{1

PROJECT_NAME = 'transquation'
PROJECT_ROOT = path(os.path.dirname(__file__))

ADMINS = (
    ('Marco Chomut', 'marco.chomut@gmail.com'),
    ('Nathaniel Soares', 'nate@natesoares.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'equatize',
        'PORT': '5433',
    }
}


# RESTRICTED {{{1

from restricted.settings import SECRET_KEY, DATABASE_PASSWORDS

DATABASES['default']['password'] = DATABASE_PASSWORDS['default']


# ENVIRONMENT {{{1

# Hostname lists for local/dev/staging/production machines
SERVERS = {
    'DEV': ['Falcon'],
    'STAGING': [],
    'PROD': [],
}

for (key, names) in SERVERS.items():
    if socket.gethostname() in names:
        SERVER_TYPE = key
        break
else:
    SERVER_TYPE = 'PROD'

DEBUG = SERVER_TYPE == 'DEV'
if DEBUG:
    USE_ETAGS = False
    CACHE_BACKEND = 'dummy:///' if DEBUG else 'memcached://127.0.0.1:11211/'
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Now that we have sentry, we always want debug info
TEMPLATE_DEBUG = True


# PREFERENCES {{{1

ROOT_URLCONF = PROJECT_NAME + '.urls'

DEFAULT_FROM_EMAIL = 'webmaster@equatize.com'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# WEBSITE {{{1

SITE_ID = 1
INTERNAL_IPS = ('127.0.0.1',)


# STATIC FILES {{{1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_ROOT + '/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

MEDIA_BUNDLES = (
    ('main.css',
        'equatize/css/reset.css',
        'equatize/css/scaffold.css',
        'jquery/ui/theme.css',
    ),
    ('main.js',
        'jquery/1.4.4.min.js',
        'jquery/ui/1.8.6.min.js',
        'modernizr/1.6.min.js',
    ),
)

MEDIA_DEV_MODE = DEBUG
GLOBAL_MEDIA_DIRS = (MEDIA_ROOT,)
GENERATED_MEDIA_DIR = '.generated_media'
PRODUCTION_MEDIA_URL = '/media/'

ROOT_MEDIA_FILTERS = {
    'css': 'mediagenerator.filters.yuicompressor.YUICompressor',
    'js': 'mediagenerator.filters.closure.Closure',
}

YUICOMPRESSOR_PATH = os.path.join(MEDIA_ROOT, 'yuicompressor', 'yuicompressor-2.4.2.jar')
CLOSURE_COMPILER_PATH = os.path.join(MEDIA_ROOT, 'closure', 'compiler.jar')


# TEMPLATES {{{1

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

@setting
def TEMPLATE_CONTEXT_PROCESSORS():
    yield 'django.core.context_processors.auth'
    yield 'django.core.context_processors.media'
    yield 'django.core.context_processors.request'
    if USE_I18N:
        yield 'django.core.context_processors.i18n'
    if DEBUG:
        yield 'django.core.context_processors.debug'

@setting
def TEMPLATE_DIRS():
    yield path(PROJECT_ROOT, 'templates')
    for root, dirs, files in os.walk(PROJECT_ROOT):
        if 'templates' in dirs:
            yield path(root, 'templates')


# MIDDLEWARE {{{1

@setting
def MIDDLEWARE_CLASSES():
    yield 'django.middleware.gzip.GZipMiddleware'
    if DEBUG:
        yield 'mediagenerator.middleware.MediaMiddleware'
    # yield 'django.middleware.cache.UpdateCacheMiddleware'
    yield 'django.middleware.http.ConditionalGetMiddleware'
    yield 'django.middleware.common.CommonMiddleware'
    yield 'django.contrib.sessions.middleware.SessionMiddleware'
    yield 'django.middleware.csrf.CsrfViewMiddleware'
    # yield 'django.middleware.locale.LocaleMiddleware',
    yield 'django.contrib.auth.middleware.AuthenticationMiddleware'
    if DEBUG:
        yield 'debug_toolbar.middleware.DebugToolbarMiddleware'
    yield 'django.contrib.messages.middleware.MessageMiddleware'
    # yield 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # yield 'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    yield 'xframeoptions.middleware.Header'
    # yield 'django.middleware.transaction.TransactionMiddleware',


# APPS {{{1

@setting
def INSTALLED_APPS():
    # Django Contrib
    yield 'django.contrib.admin'
    yield 'django.contrib.admindocs'
    yield 'django.contrib.auth'
    # yield 'django.contrib.comments'
    yield 'django.contrib.contenttypes'
    # yield 'django.contrib.databrowse' # read-only version of the admin
    # yield 'django.contrib.flatpages'
    yield 'django.contrib.humanize'
    yield 'django.contrib.markup' # includes textile, markdown, ReST
    yield 'django.contrib.messages'
    # yield 'django.contrib.redirects' # db-level redirects
    yield 'django.contrib.sessions'
    # yield 'django.contrib.sitemaps'
    yield 'django.contrib.sites'
    # yield 'django.contrib.syndication'
    yield 'django.contrib.webdesign' # lorem ipsum generator
    
    # Third-Party
    yield 'django_extensions'
    yield 'indexer'
    yield 'mediagenerator'
    yield 'paging'
    yield 'sentry'
    yield 'sentry.client'
    yield 'south'
    yield 'xframeoptions'
    if DEBUG:
        yield 'debug_toolbar'

    # Equatize

LOGIN_REDIRECT_URL = '/'

X_FRAME_OPTIONS = 'SAMEORIGIN'

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
