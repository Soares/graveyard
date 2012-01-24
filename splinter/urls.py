from django.conf.urls.defaults import *
from django.contrib import admin
from local.urls import urlpatterns
from splinter.entries import views as entries
admin.autodiscover()

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
	(r'^$', entries.latest),
	(r'^entry/(?P<slug>[-\w]+)/$', entries.entry),
	(r'^tag/(?P<slug>[-\w]+)/$', entries.tag),
)
