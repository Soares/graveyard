from django.db import models
from datetime import timedelta
from utilities.forms.fields import TimeDeltaField as TimeDeltaFormField
from utilities.models import encode, decode
import json

class TimeDeltaField(models.IntegerField):
    """
    A field for storing timedelta objects

    >>> field = TimeDeltaField()
    >>> delta = timedelta(days=10, seconds=11)
    >>> encoded = field.get_db_prep_save(delta)
    >>> decoded = field.to_python(encoded)
    >>> delta == decoded
    True
    >>> delta = timedelta(seconds=8)
    >>> encoded = field.get_db_prep_save(delta)
    >>> decoded = field.to_python(encoded)
    >>> delta == decoded
    True
    """
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value is None or isinstance(value, timedelta):
            return value
        return timedelta(seconds=value)

    def get_db_prep_save(self, value):
        if isinstance(value, int):
            return value
        return 60*60*24*value.days + value.seconds

    def formfield(self, *args, **kwargs):
        kwargs.setdefault('form_class', TimeDeltaFormField)
        return super(TimeDeltaField, self).formfield(*args, **kwargs)


class DictField(models.TextField):
    """
    Only supports JSON serializable items in the dictionary.
    It is smart enough to encode models by type and id transparently,
    so you can use models too.
    However, if you create a circular relationship
    (model -> dict field -> same model) you'll get yourself a stack overflow.
    In this case, encode the models yourself.
    """
    __metaclass__ = models.SubfieldBase
    _deflated = '_deflated'

    def inflate(self, dict):
        for (key, value) in dict.iteritems():
            if isinstance(value, list) and value[0] == self._deflated:
                dict[key] = decode(value[1]).objects.get(pk=value[2])
        return dict

    def deflate(self, value):
        def deflated(item):
            if isinstance(item, models.Model):
                return [self._deflated, encode(item.__class__), item.pk]
            return item
        return dict((k, deflated(v)) for (k, v) in value.items())

    def to_python(self, value):
        if value is None:
            return {}
        elif isinstance(value, dict):
            return self.inflate(value)
        return self.inflate(json.loads(value or '{}'))

    def get_db_prep_save(self, value):
        if isinstance(value, str):
            return value
        return json.dumps(self.deflate(value or {}), indent=None)
