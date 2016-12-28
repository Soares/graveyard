from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('activator.views',
    url(r'^activate/(?P<type>\d+)/done/$', 'activated', name='activated'),
    url(r'^activate/(?P<type>\d+)/(?P<token>\w+)/$', 'activate', name='activate'),
    url(r'^request/(?P<type>\d+)/done/$', 'requested', name='requested'),
    url(r'^request/(?P<type>\d+)/$', 'request', name='request'),
)
