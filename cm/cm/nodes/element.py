from itertools import chain
from node import Node, Body, is_node
from cm.utilities import ListDict
from cm.exceptions import ConversionError


class Element(Node):
    def __init__(self, tag, properties, args, attributes):
        self.tag, self.args = tag, args
        self.close, self.strip, self.body = False, False, None
        self.attributes = ListDict()
        for (name, value) in attributes:
            self.attributes.add(name, value)
        for (name, value) in properties:
            self.attributes.add(name, value)
        self.oneline = False

    def set_mode(self, mode):
        self.close = '/' in mode
        self.strip = '>' in mode

    def consumes_body(self):
        return self.body is None and not self.close

    def set_body(self, *statements):
        if self.close:
            raise ConversionError('You are trying to put a body '
                                  'in a self-closing tag.')
        self.body = Body(*statements)

    def sections(self):
        for arg in filter(is_node, self.args):
            for s in arg.sections():
                yield s
        for v in filter(is_node, chain(self.attributes.lists())):
            for s in v.sections():
                yield s
        if self.body:
            for s in self.body.sections():
                yield s

    def showhead(self):
        mode = '/' if self.close else ''
        mode += '>' if self.strip else ''
        return 'Element: %s%s' % (self.tag, mode)

    def children(self):
        extra = self.body.statements if self.body else ()
        return chain(self.attributes.items(), extra)

    def evaluate(self, settings):
        attrs = self.attributes.dict().items()
        attrs = dict((k, map(settings.eval, vs)) for (k, vs) in attrs)
        body = settings.eval(self.body)
        renderer = settings.element(self.tag)
        args = map(settings.eval, self.args)
        return renderer(self.tag, args, attrs, body,
                        self.close, self.strip, self.oneline, settings)
