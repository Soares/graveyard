from environment import DEBUG

@tuple
@apply
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
  # if DEBUG:
  #     yield 'debug_toolbar.middleware.DebugToolbarMiddleware'
    yield 'django.contrib.messages.middleware.MessageMiddleware'
  # yield 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
  # yield 'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    yield 'xframeoptions.middleware.Header'
  # yield 'django.middleware.transaction.TransactionMiddleware',
