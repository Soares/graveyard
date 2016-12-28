import os
from os.path import normpath, join
from environment import PROJECT_ROOT, DEBUG, USE_I18N

loaders = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
cacher = 'django.templates.loaders.cached.Loader'
#TEMPLATE_LOADERS = loaders if DEBUG else (cacher, loaders)
TEMPLATE_LOADERS = loaders


# Allows sentry to log template syntax errors
TEMPLATE_DEBUG = True


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)
if USE_I18N: TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.i18n',
)
if DEBUG: TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.debug',
)

root_dir = normpath(join(PROJECT_ROOT, 'templates'))
app_dirs = tuple(normpath(join(root, 'templates'))
            for (root, dirs, files) in os.walk(PROJECT_ROOT)
            if 'templates' in dirs)
TEMPLATE_DIRS = (root_dir,) + app_dirs
