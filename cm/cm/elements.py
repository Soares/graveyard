from cm.library import Library
from utilities import indent
library = Library()

def closer(tag, attributes, settings):
    return Element(tag, (), attributes, '', close=True, settings=settings)


class Element:
    arguments = ()

    def __init__(self, tag, args=(), attributes={}, body='',
            close=False, strip=False, oneline=False, settings=None):
        self.tag, self.args, self.attributes = tag, args, attributes
        self.body, self.close, self.strip = body, close, strip
        self.oneline, self.settings = oneline, settings
        self.args = self.map_args(*self.arguments)
        self.setup()
        self.render()

    def setup(self):
        pass

    def render(self):
        if self.args:
            raise TypeError('Element %s can not handle arguments %s' %
                            (self.tag, self.args))
        if self.close and self.body.strip():
            raise ValueError('This %s element can not have a body.' % self.tag)
        attrs = self.render_attributes()
        body = self.body.strip() if self.strip else self.body
        if self.close:
            closer = '/' if self.settings.filetype == 'xhtml' else ''
            self.rendered = '<{0}{1}{2}>'.format(self.tag, attrs, closer)
        else:
            self.rendered = self.settings.join((
                '<{0}{1}>'.format(self.tag, attrs),
                    indent(body.strip() if self.strip else body),
                '</{0}>'.format(self.tag),
            ), compress=self.strip or self.oneline)

    def map_args(self, *names):
        for (name, arg) in zip(names, self.args):
            self.attributes.setdefault(name, []).append(arg)
        return self.args[len(names):]

    def render_attributes(self):
        def isflag((k, vs)):
            return len(vs) is 1 and vs[0] is True
        def flag((k, vs)):
            return '{0}="{0}"'.format(k) if verbose else k
        def isattribute((k, vs)):
            stripped = filter(bool, (str(v).strip() for v in vs))
            return not isflag((k, vs)) and len(list(stripped))
        def attribute((k, vs)):
            joined = ' '.join(map(str, vs))
            c1, c2 = joined.count("'"), joined.count('"')
            string = ("'{0}'" if c2 > c1 else '"{0}"').format(joined)
            return '{0}={1}'.format(k, string)
        verbose = self.settings.filetype == 'xhtml'
        items = self.attributes.items()
        flags = ' '.join(map(flag, filter(isflag, items)))
        attrs = ' '.join(map(attribute, filter(isattribute, items)))
        prefix = lambda s: ' {0}'.format(s).rstrip()
        return prefix(flags) + prefix(attrs)

    def __str__(self):
        return self.rendered


def remap(newtag):
    class Remap(Element):
        def setup(self):
            self.tag = newtag
    return Remap


class AutoCloser(Element):
    def setup(self):
        self.close = True


def input(type):
    class Input(AutoCloser):
        arguments = 'value',
        def setup(self):
            self.attributes.setdefault('type', []).append(type)
            self.tag = 'input'
    return Input


library.register('realbutton', remap('button'))
library.register('submit', input('submit'))
library.register('button', input('button'))
library.register('password', input('password'))
library.register('hidden', input('hidden'))
library.register('text', input('text'))
library.register('radio', input('radio'))
library.register('checkbox', input('checkbox'))
for tag in 'input', 'meta', 'link', 'br', 'hr':
    library.register(tag, AutoCloser)


@library.register('a')
class A(Element):
    arguments = 'href',

@library.register('img')
class Img(AutoCloser):
    arguments = 'src',

@library.register('form')
class Form(Element):
    arguments = 'action', 'method'

@library.register('label')
class Label(Element):
    arguments = 'for',


@library.register('sass')
class Sass(Element):
    def setup(self):
        from sass import sass
        compression = 'compressed' if self.settings.compress else 'nested'
        sasser = self.settings.configuration('sass')
        self.body = sass(self.body, sasser, compression=compression)
        self.attributes.setdefault('type', []).append('text/css')
        self.tag = 'style'
