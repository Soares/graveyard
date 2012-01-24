from django import forms
from datetime import timedelta
from django.utils.safestring import mark_safe

class TimeDeltaInput(forms.widgets.Input):
    def render(self, name, value, attrs=None):
        if value is None:
            days, seconds = None, None
        if isinstance(value, int):
            value = timedelta(seconds=value)
        if isinstance(value, timedelta):
            days, seconds = value.days, value.seconds
        days = super(TimeDeltaInput, self).render(name + '_days', days, attrs)
        seconds = super(TimeDeltaInput, self).render(name + '_seconds', seconds, attrs)
        return mark_safe(days + ' ' + seconds)

    def value_from_datadict(self, data, files, name):
        days = data.get('%s_days' % name)
        seconds = data.get('%s_seconds' % name)
        if days is seconds is None:
            return None
        elif days is None:
            return timedelta(seconds=seconds)
        elif seconds is None:
            return timedelta(days)
        return timedelta(days, seconds)


class CheckboxInput(forms.widgets.CheckboxInput):
    def render(self, name, value, attrs=None):
        self.label = getattr(self, 'label', False) or self.attrs.pop('label')
        old = super(CheckboxInput, self).render(name, value, attrs)
        return mark_safe(u'<label>%s %s</label>' % (old, self.label))
