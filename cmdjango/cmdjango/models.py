from django.db import models
from utilities.templatetags.utils import safe_markdown
from django.contrib.sites.models import Site


class Tidbit(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = 'name',
        abstract = True

    def render(self, **context):
        context.setdefault('site', Site.objects.get_current())
        return self.content.format(**context)

    def __unicode__(self):
        return self.name


class Text(Tidbit):
    content = models.TextField()

    def render(self, **context):
        return safe_markdown(super(Text, self).render(**context))


class Line(Tidbit):
    content = models.CharField(max_length=255)

    def render(self, **context):
        return super(Line, self).render(**context).strip()


from cmdjango.functions import library, gettext
from functools import partial
library.register('text', partial(gettext, Text))
library.register('line', partial(gettext, Line))
