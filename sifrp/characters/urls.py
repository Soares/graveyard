from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('characters.views',
    url(r'^$', 'new'),
    url(r'^(?P<id>\d+)/', 'edit'),
)

