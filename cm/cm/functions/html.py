from cm.library import Library, give_settings
from cm.elements import closer
import re
library = Library()

r = lambda regex: re.compile(r'^\s*%s\s*$' % regex, re.IGNORECASE)

doctypes = (
    (r('(html)?\s*5'),
        '<!DOCTYPE HTML>', 'html'),
    (r('(html)?(\s*4(.01)?)?(\s*s(trict)?)?'),
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
        '"http://www.w3.org/TR/html4/strict.dtd">', 'html'),
    (r('(html)?(\s*4(.01)?)?\s*t(rans(itional)?)?'),
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" '
        '"http://www.w3.org/TR/html4/loose.dtd">', 'html'),
    (r('(html)?(\s*4(.01)?)?\s*f(rame(s(et)?)?)?'),
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" '
        '"http://www.w3.org/TR/html4/frameset.dtd">', 'xhtml'),
    (r('x(html)?\s*(1(.0)?)?(\s*s(trict)?)?'),
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '
        '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">', 'xhtml'),
    (r('x(html)?\s*(1(.0)?)?\s*t(rans(itional)?)?'),
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
        '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">', 'xhtml'),
    (r('x(html)?\s*(1(.0)?)?\s*f(rame(s(et)?)?)?'),
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" '
        '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">', 'xhtml'),
    (r('x(html)?\s*1.1'),
        '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" '
        '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">', 'xhtml'))

def parse_doctype(type):
    for (regex, doctype, type) in doctypes:
        if regex.match(str(type)):
            return doctype, type
    from cm.exceptions import ConversionError
    raise ConversionError('Unrecognized doctype: %s' % type)


@library.register
@give_settings
def doctype(type='HTML', silent=False, settings=None):
    doctype, settings.filetype = parse_doctype(type)
    return '' if silent else doctype


@library.register
@give_settings
def encoding(type='text/html;charset=UTF-8', settings=None):
    if settings.filetype != 'html':
        return ''
    return closer('meta', {
        'http-equiv': ['Content-type'], 'content': [type]
    }, settings)


@library.register
@give_settings
def favicon(name='favicon.png', root=None, settings=None):
    root = root or settings.context['images']
    return closer('link', {
        'rel': ['icon'], 'type': ['image/png'],
        'href': ['%s/%s' % (root, name)],
    }, settings)


@library.register
@give_settings
def style(*names, **kwargs):
    settings = kwargs['settings']
    root = kwargs.get('root', settings.context['media'])
    dir = (kwargs.pop('in') if 'in' in kwargs else '').rstrip('/')
    dir = (dir + '/') if dir else ''
    rename = lambda name: dir + name + ('' if name.endswith('.css') else '.css')
    return settings.join(closer('link', {
        'rel': ['stylesheet'], 'type': ['text/css'],
        'href': ['%scss/%s' % (root, rename(name))],
    }, settings) for name in names)


@library.register
@give_settings
def script(*names, **kwargs):
    settings = kwargs['settings']
    root = kwargs.get('root', settings.context['media'])
    dir = (kwargs.pop('in') if 'in' in kwargs else '').rstrip('/')
    dir = (dir + '/') if dir else ''
    rename = lambda name: dir + name + ('' if name.endswith('.js') else '.js')
    def render(name):
        return '<script type="text/javascript" src="{0}js/{1}">'\
               '</script>'.format(root, rename(name))
    return settings.join(map(render, names))
