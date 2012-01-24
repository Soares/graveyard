from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from cm.library import Library, give_cm
from cm import functions
library = Library()


def gettext(type, _name, _default='', **kwargs):
    text, created = type.objects.get_or_create(name=_name)
    text.content = text.content or _default
    text.save()
    return text.render(**kwargs) or mark_safe('"<a href="{0}">{1}</a>"'.format(
        reverse('admin:cmdjango_{0}_change'.format(
            text.__class__.__name__.lower()), args=[text.pk]), _name))


@library.register('')
@give_cm
def tag(*contents, **kwargs):
    contents = [c if i % 2 else '{{%{0}%}}'.format(c) for (i, c) in enumerate(contents)]
    cm, compress = kwargs.pop('cm'), kwargs.get('c', False)
    return cm.join(contents, compress)


@library.register
@give_cm
def doctype(type='HTML', silent=False, cm=None):
    from cm.functions import html
    doctype, filetype = html.parse_doctype(type)
    load = '{%load filetype%}'
    set = '{{%filetype "{0}"%}}'.format(filetype)
    return cm.join((load, set, html.doctype(type, silent, cm)))


library.register('get', functions.get, evaluate=False)
library.register('gethard', functions.gethard)
library.register('val', lambda contents: '{{%s}}' % contents)
library.register('url', lambda object: '{{' + object + '.get_absolute_url}}')
