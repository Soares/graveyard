from functools import update_wrapper
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from utilities.decorators import decorator
from django.contrib.auth.decorators import login_required as auth_login_required

@decorator
def ajax(fn, request, *args, **kwargs):
    if request.method.is_ajax():
        return fn(request, *args, **kwargs)
    raise Http404


def gets(model):
    @decorator
    def view(fn, request, pk, *args, **kwargs):
        object = get_object_or_404(model, pk=pk)
        return fn(request, object, *args, **kwargs)
    return view


def login_required(fn):
    @auth_login_required
    def view(request, *args, **kwargs):
        return fn(request, *args, **kwargs) if request.user.profile else redirect('meta.views.home')
    update_wrapper(view, fn)
    return view
