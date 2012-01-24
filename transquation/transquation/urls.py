from settings import path
from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^equatize/', include('equatize.foo.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'django.views.generic.simple.direct_to_template',
        {'template': 'main.html'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^tinymce/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': path(settings.MEDIA_ROOT, 'tinymce-dev', 'jscripts', 'tiny_mce')}),
        (r'^%s/(?P<path>.*\.(?!js|css).*)$' % settings.MEDIA_URL, 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
