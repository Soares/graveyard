import os.path
from environment import DEBUG

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    'django_extensions',
    'indexer',
    'mediagenerator',
    'paging',
    'sentry',
    'sentry.client',
    'south',
    'hisp',
    'xframeoptions',

    'characters',
)

if DEBUG: INSTALLED_APPS += (
    'django.contrib.webdesign',
   #'debug_toolbar',
)
 

# Admin
from media import MEDIA_URL
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'


# Auth
LOGIN_URL = 'auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = 'auth/login/error/'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.contrib.orkut.OrkutBackend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)


# Sites
SITE_ID = 1


# XFrame Options
X_FRAME_OPTIONS = 'SAMEORIGIN'


# Debug Toolbar
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

# Media Generator
from media import MEDIA_ROOT, MEDIA_URL
from environment import PROJECT_NAME
MEDIA_DEV_MODE = DEBUG
GLOBAL_MEDIA_DIRS = (MEDIA_ROOT,)
DEV_MEDIA_URL = MEDIA_URL
aws = 'http://so8res.s3-website-us-east-1.amazonaws.com/'
PRODUCTION_MEDIA_URL = aws + PROJECT_NAME + '/'
ROOT_MEDIA_FILTERS = {
    'css': 'mediagenerator.filters.yuicompressor.YUICompressor',
    'js': 'mediagenerator.filters.closure.Closure',
}
YUICOMPRESSOR_PATH = os.path.join(MEDIA_ROOT, 'tools', 'yuicompressor', '2.4.2.jar')
CLOSURE_COMPILER_PATH = os.path.join(MEDIA_ROOT, 'tools', 'closure', 'compiler.jar')
