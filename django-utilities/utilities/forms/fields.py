import re
from django import forms
from django.contrib.auth.models import User
from utilities.forms.widgets import TimeDeltaInput, CheckboxInput

class UsernameField(forms.CharField):
    errors = {
        'not_unique': 'Please enter a unique username',
        'does_not_exist': 'That user does not exist',
    }

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 30
        self.new = kwargs.pop('new', True)
        super(UsernameField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(UsernameField, self).clean(value)
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            is_new = True
        else:
            is_new = False
        if is_new != self.new:
            raise forms.ValidationError(self.errors['not_unique' if self.new else 'does_not_exist'])
        return value


class TimeDeltaField(forms.IntegerField):
    regex = re.compile(r'((\d+) days?, )?(\d{1,2}):(\d\d):(\d\d)')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', TimeDeltaInput)
        super(TimeDeltaField, self).__init__(*args, **kwargs)

    def clean(self, value):
        try:
            return int(value)
        except ValueError:
            pass
        match = self.regex.match(value)
        if not match:
            raise forms.ValidationError('Please enter a timedelta in [# day[s], ]h[h]:mm:ss format or in just seconds')
        _, days, hours, minutes, seconds = map(lambda i: int(i) if i else 0, match.groups())
        return days*24*60*60 + hours*60*60 + minutes*60 + seconds


class BooleanField(forms.BooleanField):
    label_inside = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', CheckboxInput)
        super(BooleanField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        return dict(super(BooleanField, self).widget_attrs(widget), label=self.label)

    def update_label(self, label):
        self.label = label
        self.widget.attrs['label'] = self.label
