"""Social auth models"""
import warnings
from datetime import timedelta

from django.db import models
from django.conf import settings

from authenticator.fields import JSONField

# If User class is overridden, it *must* provide the following fields,
# or it won't be playing nicely with django.contrib.auth module:
#
#   id         = AutoField()
#   last_login = DateTimeField()
#   is_active  = BooleanField()
#
# and methods:
#
#   def is_authenticated():
#       ...
RECOMMENDED_FIELDS = ('last_login', 'is_active')
RECOMMENDED_METHODS = ('is_authenticated',)

if getattr(settings, 'AUTHENTICATOR_USER_MODEL', None):
    SimpleUser = models.get_model(*settings.AUTHENTICATOR_USER_MODEL.split('.'))
    missing = list(set(RECOMMENDED_FIELDS) -
                   set(SimpleUser._meta.get_all_field_names())) + \
              [name for name in RECOMMENDED_METHODS
                      if not callable(getattr(SimpleUser, name, None))]
    if missing:
        warnings.warn('Missing recommended attributes or methods '\
                      'in custom User model: "%s"' % ', '.join(missing))
else:
    from django.contrib.auth.models import User as SimpleUser


def isuserproxy(model):
    """
    Determine if a model is a User or a proxy thereof.
    isinstance won't work for various reasons, namely,
    isinstance is retarded in Python
    """
    from django.contrib.contenttypes.models import ContentType
    upk = ContentType.objects.get_for_model(User)
    mpk = ContentType.objects.get_for_model(model)
    return upk == mpk


class UserManager(SimpleUser.objects.__class__):
    def with_email(self, email):
        if email: # '' should be treated as a null email
            return self.get(authgroups__email=email)
        raise self.model.DoesNotExist("could not find user with email %s" % email)


class User(SimpleUser):
    objects = UserManager()

    class Meta:
        proxy = True

    @property
    def authenticators(self):
        return ExternalAuth.objects.filter(group__user=self)

    @property
    def email(self):
        try:
            return self.authgroups.all()[0].email
        except IndexError:
            raise AttributeError("User %s has no email." % self)

    @property
    def emails(self):
        return self.authgroups.values_list('email', flat=True)

    def add_email(self, email, primary=None):
        """
        If primary is None, primary will be True this is the user's first
        email address. Set primary to False to prevent his behavior.
        """
        if primary is None and self.authgroups.count() == 0:
            primary = True
        primary = bool(primary)
        if primary:
            self.authgroups.filter(primary=True).update(primary=False)
        email = email or None
        try:
            group = self.authgroups.get(email=email)
        except self.authgroups.model.DoesNotExist:
            group = self.authgroups.create(email=email, primary=primary)
        if group.primary != primary:
            group.primary = primary
            group.save()
        return group

    def send_email(self, subject, message, sender=None):
        from django.core.mail import send_mail
        from django.conf import settings
        sender = sender or settings.DEFAULT_FROM_EMAIL
        return send_mail(subject, message, sender, [self.email])

    def merge_into(self, user):
        try:
            self.delete()
        except models.ProtectedError as e:
            for obj in e.protected_objects:
                try:
                    obj.switch_user(user)
                except AttributeError:
                    fks = filter(lambda f: isinstance(f, models.ForeignKey), obj._meta.fields)
                    ufks = filter(lambda f: isuserproxy(f.rel.to), fks)
                    objfks = filter(lambda f: getattr(obj, f.name, None) == self, ufks)
                    for field in objfks:
                        setattr(obj, field.name, user)
                    obj.save()
        self.delete()


class AuthGroup(models.Model):
    user = models.ForeignKey(User, related_name='authgroups', on_delete=models.PROTECT)
    email = models.EmailField(unique=True, blank=True, null=True)
    primary = models.BooleanField(default=False)

    class Meta:
        ordering = ('-primary', 'email')

    def __unicode__(self):
        return self.email or '[no email]'

    def switch_user(self, user):
        group = user.add_email(self.email)
        self.externalauths.update(group=group)
        self.delete()

    def save(self, *args, **kwargs):
        if self.email == '':
            self.email = None
        return super(AuthGroup, self).save(*args, **kwargs)


class ExternalAuth(models.Model):
    group = models.ForeignKey(AuthGroup, related_name='externalauths')
    fullname = models.CharField(max_length=100, blank=True, default='')
    nickname = models.CharField(max_length=100, blank=True, default='')
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=255)
    extra_data = JSONField(blank=True)

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')

    def __unicode__(self):
        """Return associated user unicode representation"""
        name = self.group.user.name or self.nickname or self.fullname or self.group.user
        return unicode(name)

    def expiration_delta(self):
        """Return saved session expiration seconds if any. Is retuned in
        the form of a timedelta data type. None is returned if there's no
        value stored or it's malformed.
        """
        if self.extra_data:
            name = getattr(settings, 'AUTHENTICATOR_EXPIRATION', 'expires')
            try:
                return timedelta(seconds=int(self.extra_data.get(name)))
            except (ValueError, TypeError):
                pass
        return None


class Nonce(models.Model):
    """One use numbers"""
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)

    def __unicode__(self):
        """Unicode representation"""
        return self.server_url


class Association(models.Model):
    """OpenId account association"""
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)  # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    def __unicode__(self):
        """Unicode representation"""
        return '%s %s' % (self.handle, self.issued)
