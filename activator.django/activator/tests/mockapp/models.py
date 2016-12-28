from django.conf import settings
from django.db import models
from forms import SimpleRequestForm

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.email

    def is_authenticated(self):
        return self.is_active

    def send_email(self, subject, message, sender=None):
        from django.core.mail import send_mail
        send_mail(subject, message, sender or settings.DEFAULT_FROM_EMAIL, [self.email])


# activator.models can't be imported until after User exists
from activator.models import ActivationRequest

class SimpleRequest(ActivationRequest):
    name = 'simple'
    formclass = SimpleRequestForm

    def activate(self, request):
        self.user.is_active = True
        self.user.save()
