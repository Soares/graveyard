import random
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import render
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from datetime import datetime, timedelta

# If User class is overridden, it must play nice with django.contrib.auth
# It must also provide a send_email(subject, message[, sender]) method.
if getattr(settings, 'ACTIVATOR_USER_MODEL', None):
    if isinstance(settings.ACTIVATOR_USER_MODEL, type):
        User = settings.ACTIVATOR_USER_MODEL
    elif len(settings.ACTIVATOR_USER_MODEL.split('.')) == 2:
        # The replication of the splitting here is better than creating a
        # top-level global variable
        User = models.get_model(*settings.ACTIVATOR_USER_MODEL.split('.'))
    else:
        User = None
    if not User:
        raise ImproperlyConfigured("Invalid user model '%s'" % settings.ACTIVATOR_USER_MODEL)
else:
    from django.contrib.auth.models import User


def get_site():
    from django.core.exceptions import ImproperlyConfigured
    try:
        return Site.objects.get_current()
    except ImproperlyConfigured:
        return None

ROOT = 'activator/'
EMAIL_MASK = ROOT + 'emails/%s.txt'
SUBJECT_MASK = ROOT + 'emails/%s-subject.txt'
REQUEST_MASK = ROOT + '%s.html'
REQUESTED_MASK = ROOT + '%s-sent.html'
ACTIVATED_MASK = ROOT + '%s-confirmed.html'


class ActivationReusedException(Exception):
    pass


class ActivationRequestManager(models.Manager):
    def request(self, user, email=None):
        record = self.create(user=user, email=email)
        record.set_token()
        record.send_email()
        record.save()
        return record


class ActivationRequest(models.Model):
    type = property(lambda self: ContentType.objects.get_for_model(self).pk)
    timeframe = timedelta(7)
    login_required = False

    user = models.ForeignKey(User)
    email = models.EmailField(blank=True, null=True)
    sent = models.DateTimeField(default=datetime.now)
    token = models.CharField(max_length=40, blank=True)
    used = models.DateTimeField(blank=True, null=True)

    objects = ActivationRequestManager()

    email_template = classmethod(lambda self: EMAIL_MASK % self.name)
    subject_template = classmethod(lambda self: SUBJECT_MASK % self.name)
    request_template = classmethod(lambda self: REQUEST_MASK % self.name)
    requested_template = classmethod(lambda self: REQUESTED_MASK % self.name)
    activated_template = classmethod(lambda self: ACTIVATED_MASK % self.name)
    error_template = ROOT + 'error.html'

    class Meta:
        abstract = True

    def __unicode__(self):
        return '<%s for %s>' % (self.__class__.__name__, self.user or self.email)

    @property
    def expires(self):
        return self.sent + self.timeframe

    def activate(self, request):
        pass
    
    def set_token(self):
        from django.utils.hashcompat import sha_constructor
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        email = self.email or self.user.email
        self.token = sha_constructor(salt+email).hexdigest()
        self.save()

    def send_email(self, sender=None):
        email = self.email or self.user.email
        context = {
            'activation_request': self,
            'site': get_site(),
        }
        message = render_to_string(self.email_template(), context)
        subject = render_to_string(self.subject_template(), context)
        subject = ''.join(subject.splitlines())
        from django.core.mail import send_mail
        sender = sender or settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, sender, [email])

    def use(self, request):
        if self.used:
            raise ActivationReusedException("Activation Request used more than once.")
        self.activate(request)
        self.used = datetime.now()
        self.save()

    @models.permalink
    def get_requested_url(self):
        return ('activator.views.requested', [self.type])

    @models.permalink
    def get_activate_url(self):
        return ('activator.views.activate', [self.type, self.token])

    @models.permalink
    def get_activated_url(self):
        return ('activator.views.activated', [self.type])

    @classmethod
    def render_request(cls, request, form):
        return render(request, cls.request_template(), {'form': form, 'site': get_site()})

    @classmethod
    def render_requested(cls, request):
        return render(request, cls.requested_template(), {'site': get_site()})

    @classmethod
    def render_error(cls, request, error):
        return render(request, cls.error_template(), {'error': error, 'site': get_site()})

    @classmethod
    def render_success(cls, request):
        return render(request, cls.activated_template(), {'site': get_site()})

    @classmethod
    def decorate(cls, view):
        return login_required(view) if cls.login_required else view
