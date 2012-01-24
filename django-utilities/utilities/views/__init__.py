from django.shortcuts import render_to_response
from django.template import RequestContext

def render(request, name, context=None, instance=None, processors=()):
    instclass = instance or RequestContext
    instance = instclass(request, processors=processors)
    return render_to_response(name, context, instance)
