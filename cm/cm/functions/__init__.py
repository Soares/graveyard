"""
This module contains all of the functions which are registered with the default
library. Check it out for examples. Also, check the documentation for
FallThrough to learn how to return extra data from a function.

A whole series of functions are provided which output characters that otherwise
may need escaping or may be difficult to use in certain contexts in cm files.
They are as follows:
    %space outputs a space
    %n outputs a newline
    %t outputs a tab
    %q outputs a single quote
    %qq outputs a double quote

    %op: outputs an opening parenthese (()
    %cp: outputs a closing parethese ())
    %oc: outputs an opening curly brace (})
    %cc: outputs a closing curly brace (})
    %ob: outputs an opening square bracket ([)
    %cb: outputs a closing square bracket (])
"""
from cm.library import Library, give_settings
library = Library()

class FallThrough(Exception):
    """
    FallThrough is used to return extra data from a function. Instead of
    returning, raise FallThrough with the return value, the data tag, and the
    data itself. The data will then be passed to the next function in line if
    the function accepts the data tag. To define which functions accept which
    data tags, use the receiving argument of the library's register function.
    """
    def __init__(self, result, tag, data=None, **extra):
        data = data or {}
        data.update(extra)
        self.result, self.tag, self.data = result, tag, data


escapes = (
    ('space', ' '),
    ('t', '\t'), ('n', '\n'),
    ('q', "'"), ('qq', '"'),
    ('op', '('), ('cp', ')'),
    ('oc', '{'), ('cc', '}'),
    ('ob', '['), ('cb', ']'),
)

def simple((name, retval)):
    library.register(name, lambda: retval)
list(map(simple, escapes))


@library.register(evaluate=False)
def set(name, value=True, settings=None):
    name.reference.set(settings.context.previous(), settings.eval(value))
    return ''


@library.register(evaluate=False)
def default(name, value=True, settings=None):
    from cm.reference import ReferenceMissing
    try:
        name.reference.get(settings.context)
    except ReferenceMissing:
        name.reference.set(settings.context.previous(), settings.eval(value))
    return ''


@library.register('', evaluate=False)
def get(lookup, default='', settings=None):
    from cm.reference import ReferenceMissing
    from cm.nodes import Lookup
    if not isinstance(lookup, Lookup):
        return settings.eval(lookup)
    try:
        value = lookup.reference.get(settings.context)
    except ReferenceMissing:
        return default
    return settings.eval(value)


@library.register('get')
def gethard(value):
    return value


@library.register('if')
def if_(predicate, body, else_=''):
    """
    >>> try:
    ...     if_(True, 'true', 'false')
    ... except FallThrough as e:
    ...     e.result, e.tag, e.data
    ('true', 'if', {'predicate': True})
    >>> try:
    ...     if_(False, 'true', 'false')
    ... except FallThrough as e:
    ...     e.result, e.tag, e.data
    ('false', 'if', {'predicate': False})
    """
    raise FallThrough(body if predicate else else_, 'if', predicate=predicate)

@library.register('elif', receiving='if')
def elif_(nextpred, body, predicate):
    """
    >>> def test(ifwas, elifis):
    ...     try:
    ...         elif_(elifis, 'body', ifwas)
    ...     except FallThrough as e:
    ...         return e.result, e.tag, e.data
    >>> test(True, True)
    ('', 'if', {'predicate': True})
    >>> test(True, False)
    ('', 'if', {'predicate': True})
    >>> test(False, True)
    ('body', 'if', {'predicate': True})
    >>> test(False, False)
    ('', 'if', {'predicate': False})
    """ 
    raise FallThrough(body if not predicate and nextpred else '', 'if', predicate=predicate or nextpred)

@library.register('else', receiving='if')
def else_(body, predicate):
    return body if not predicate else ''


@library.register('for', evaluate=False)
def for_(name, iter, body, settings=None):
    settings.context.push()

    iter = settings.eval(iter)
    lst = list(range(iter) if isinstance(iter, (float, int)) else iter)
    data = {'counter': 1, 'counter0': 0, 'first': True, 'last': False}
    if 'forloop' in settings.context:
        data['forloop'] = settings.context['forloop']
    settings.context['forloop'] = data
    output, length = [], len(lst)

    for e in lst:
        output.append('')
        data['first'] = False
        data['last'] = data['counter'] == length
        name.reference.set(settings.context, e)
        output[-1] += settings.eval(body)
        data['counter'] += 1
        data['counter0'] += 1

    settings.context.pop()
    raise FallThrough(settings.join(output), 'for', wasempty=length is 0)

@library.register(receiving='for')
def empty(body, wasempty):
    return body if wasempty else ''


@library.register
def comment(body, **kwargs):
    """
    >>> comment('comment')
    '<!--comment-->'
    >>> comment('comment', **{'for': 'IE'})
    '<!--[if IE]>comment<!--[endif]>'
    """
    if 'for' in kwargs:
        return '<!--[if %s]>%s<!--[endif]>' % (kwargs['for'], body)
    return '<!--%s-->' % body


@library.register
def silent(body):
    return ''


@library.register('range')
def range_(start, stop=None, step=None):
    """
    >>> range(3)
    [0, 1, 2]
    >>> range(0, 6, 2)
    [0, 2, 4]
    """
    if stop is None:
        start, stop = stop, start
    return list(range(start=start, stop=stop, step=step))


@library.register
@give_settings
def include(filename, settings, **context):
    try:
        return settings.render(filename, context)
    except Exception as e:
        from cm.exceptions import convert
        raise convert(e, filename)


@library.register
def title(string):
    return string.title()

@library.register(evaluate=False)
def macro(name, *params, **defaults):
    from cm.exceptions import ConversionError
    settings = defaults.pop('settings')
    name = settings.eval(name)
    try:
        params, body = params[:-1], params[-1]
    except IndexError:
        raise TypeError('The macro function requires a body')
    try:
        params = [param.normalize() for param in params]
    except (AttributeError, ConversionError) as e:
        raise ConversionError('Error in %s: macro parameters must be '
                              'normalized (non-dotted) variable names.' % name)
    defaults = dict((k, settings.eval(v)) for (k, v) in defaults.items())

    def macro(*args, **kwargs):
        context = dict(defaults)
        context.update(dict(zip(params[:len(args)], args)))
        context.update(kwargs)
        for required in params[len(args):]:
            if required not in context:
                raise TypeError('Macro %s requires argument %s'
                                % (name, required))
        settings.context.update(context)
        value = settings.eval(body)
        settings.context.pop()
        return value

    settings.context.globals.setdefault('macros', {})[name] = macro


@library.register
@give_settings
def call(name, *args, **kwargs):
    macros = kwargs.pop('settings').context.globals.get('macros', {})
    if name not in macros:
        raise KeyError('Could not find macro %s in %s' % (name, macros))
    return macros[name](*args, **kwargs)
