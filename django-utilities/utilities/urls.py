from django.conf.urls.defaults import url as makeurl

def url(regex, view, name=None, kwargs=None, prefix=''):
    return makeurl(regex, view, kwargs, name or view, prefix)
