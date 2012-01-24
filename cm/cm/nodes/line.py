from node import Node

class Line(Node):
    def __init__(self, indent, node, lineno):
        self.node, self.lineno = node, lineno
        self.indent, self.indentation = indent, len(indent)

    def subparse(self, builder):
        self.node.subparse(builder.parse)
        if self.node.consumes_body():
            self.node.set_body(*list(builder.parse_body()))

    def evaluate(self, *args, **kwargs):
        return self.node.evaluate(*args, **kwargs)

    def split(self):
        return self.indent, self.node

    def accepts(self, settings, falltag):
        return self.node.accepts(settings, falltag)

    def _to_string(self, sub):
        node = sub(self.node)
        if getattr(self, 'context', None):
            return '%s (line %d in %s)' % (node, self.lineno, self.context)
        return '%s (line %d)' % (node, self.lineno)

    def __repr__(self):
        return self._to_string(repr)

    def __str__(self):
        return self._to_string(str)


class EmptyLine(Node):
    def __repr__(self):
        return '(Empty Line)'

    def evaluate(self, settings):
        return '' if settings.compress else '\n'

    def __str__(self):
        return '\n'
