from datetime import datetime
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.transaction import commit_on_success

@commit_on_success
def request(request, type):
    Model = get_object_or_404(ContentType, pk=type).model_class()
    if Model.login_required and not request.user.is_authenticated():
        return redirect(settings.LOGIN_URL)
    if request.method == 'POST':
        form = Model.formclass(request.POST)
        if form.is_valid():
            try:
                user = form.get_user()
            except AttributeError:
                user = request.user
            try:
                email = form.get_email()
            except AttributeError:
                email = None
            if user:
                record = Model.objects.request(user, email)
            else:
                record = Model()
            return redirect(record.get_requested_url())
    else:
        form = Model.formclass()
    return Model.render_request(request, form)


def requested(request, type):
    Model = get_object_or_404(ContentType, pk=type).model_class()
    if Model.login_required and not request.user.is_authenticated():
        return redirect(settings.LOGIN_URL)
    return Model.render_requested(request)


@commit_on_success
def activate(request, type, token):
    Model = get_object_or_404(ContentType, pk=type).model_class()
    try:
        record = Model.objects.get(token=token)
    except Model.DoesNotExist:
        return Model.render_error(request, 'nonexistant')
    if record.expires < datetime.now():
        return Model.render_error(request, 'expired')
    if record.used:
        return Model.render_error(request, 'used')
    if request.user.is_authenticated():
        logout(request)
    user = authenticate(type=Model, token=token)
    login(request, user)
    record.use(request)
    return redirect(record.get_activated_url())


@login_required
def activated(request, type):
    Model = get_object_or_404(ContentType, pk=type).model_class()
    return Model.render_success(request)
