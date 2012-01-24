from itertools import chain
from cm.functions import FallThrough
from cm.exceptions import ConversionError, convert

def is_node(n):
    return isinstance(n, Node)


class Node(object):
    def pad(self, item, first='|--', rest='|  '):
        lines = str(item).split('\n')
        f = first + lines[0]
        r = (rest + r for r in lines[1:])
        return '\n'.join(chain([f], r))

    def consumes_body(self):
        return False

    def accepts(self, settings, falltag):
        return falltag is None

    def subparse(self, parse):
        pass

    def sections(self):
        return ()

    def showhead(self):
        return self.__class__.__name__

    def children(self):
        return ()

    def draw(self, head, *children):
        head = '+ %s' % head
        children = list(children)
        middle = map(self.pad, children[:-1])
        last = (self.pad(c, '`--', '   ') for c in children[-1:])
        return '\n'.join(chain([head], middle, last))

    def __repr__(self):
        noline = '%s(...)' % self.showhead()
        if hasattr(self, 'lineno'):
            return '%s at line %d' % (noline, self.lineno)
        return noline

    def __str__(self):
        return self.draw(self.showhead(), *self.children())


class Body(Node):
    def __init__(self, *statements):
        self.statements = statements

    def children(self):
        return self.statements

    def evaluate(self, settings, adjustment=0, exclude=()):
        from line import EmptyLine
        output = []
        falltag = None
        falldata = {}
        for statement in self.statements:
            if isinstance(statement, EmptyLine):
                # Empty lines can not raise FallThrough and should not
                # consume FallThrough data
                output.append(statement.evaluate(settings))
                continue
            if exclude and isinstance(statement.node, exclude):
                continue
            if not statement.accepts(settings, falltag):
                if falltag is None:
                    # The don't accept us sending no data
                    # This must be a follower-only function called alone
                    raise ConversionError(
                            'Function %s can not be called on its own.'
                            % statement.name)
                falldata = {}
            try:
                result = statement.evaluate(settings, **falldata)
                falltag, falldata = None, {}
            except FallThrough as e:
                result, falltag, falldata = e.result, e.tag, e.data
            except ConversionError as e:
                e.contexts.append(statement)
                raise
            except Exception as e:
                raise convert(e, statement)
            output.append(result)
        return settings.join(output)

    def sections(self):
        for statement in self.statements:
            for s in statement.sections():
                yield s

    def __len__(self):
        from line import EmptyLine
        nonempty = lambda s: not isinstance(s, EmptyLine)
        return len(list(filter(nonempty, self.statements)))
