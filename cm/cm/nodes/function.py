from node import Node, Body, is_node
from itertools import chain
from cm.exceptions import ConversionError

def check_kwargs(kwargs):
    names = []
    for (k, v) in kwargs:
        if k in names:
            raise ConversionError(
                    'You gave the same keyword argument twice: %s' % k)
        names.append(k)


class Function(Node):
    def __init__(self, name, args=(), kwargs=(), body=None):
        check_kwargs(kwargs)
        self.name, self.args, self.kwargs, = name, args, kwargs
        self.body = None if body is None else Body(body)

    def consumes_body(self):
        return self.body is None

    def set_body(self, *statements):
        self.body = Body(*statements)

    def mentors(self, other):
        return isinstance(other, Function)

    def showhead(self):
        return 'Function: %s' % self.name

    def sections(self):
        for arg in filter(is_node, self.args):
            for s in arg.sections():
                yield s
        for v in filter(is_node, dict(self.kwargs).values()):
            for s in v.sections():
                yield s
        if self.body:
            for s in self.body.sections():
                yield s

    def children(self):
        args = ('arg: \n%s' % a for a in self.args)
        kwargs = ('kwarg (%s): \n%s' % a for a in self.kwargs)
        return chain(args, kwargs, self.body.statements if self.body else ())

    def accepts(self, settings, tag):
        return settings.accepts(self.name, tag)

    def evaluate(self, settings, **fallthrough):
        settings.context.push()
        function = settings.function(self.name)
        evaluate = getattr(function, 'evaluate', True)
        eval = (lambda n: settings.eval(n)) if evaluate else (lambda n: n)
        args = list(map(eval, self.args))
        if self.body:
            args.append(eval(self.body))
        kwargs = dict((k, eval(v)) for (k, v) in self.kwargs)
        kwargs.update(fallthrough)
        if getattr(function, 'give_settings', False) or not evaluate:
            kwargs['settings'] = settings
        elif getattr(function, 'give_context', False):
            kwargs['context'] = settings.context
        result = function(*args, **kwargs)
        settings.context.pop()
        return settings.eval(result)
