from node import Node, Body

class Parent(object):
    def __init__(self, evaluated, oldparent=None):
        if oldparent:
            self.parent = oldparent
        self.evaluated = evaluated

    def __str__(self):
        return self.evaluated


class Section(Node):
    def __init__(self, name, mode=''):
        self.name = name
        self.body = None
        self.child, self.parent = None, None
        self.mode = mode
        self.above = mode.count('+')
        self.below = mode.count('-')

    def sections(self):
        if self.body:
            for s in self.body.sections():
                yield s
        yield self

    def become(self, section):
        self.child = section
        section.parent = self

    def consumes_body(self):
        return self.body is None

    def set_body(self, *statements):
        self.body = Body(*statements)

    def showhead(self):
        return 'Section: %s%s' % (self.name, self.mode)

    def children(self):
        return self.body.statements if self.body else ()

    def evaluate(self, settings, passdown=True):
        if passdown and self.child:
            return self.child.evaluate(settings)
        settings.context.push()
        result = settings.eval(self.body)
        if self.parent:
            if self.above or self.below:
                parent = self.parent.evaluate(settings, passdown=False)
                oldparent = settings.context.get('parent')
                settings.context['parent'] = Parent(parent, oldparent)
            for _ in range(self.above):
                result = parent + result
            for _ in range(self.below):
                result += parent
        settings.context.pop()
        return result
