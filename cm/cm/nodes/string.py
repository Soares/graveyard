from cm.exceptions import ConversionError
from cm.reference import Reference, ReferenceMissing
from cm.functions import FallThrough
from node import Node
import re

lookup = re.compile(r'(?<!\\)\$([a-zA-Z][a-zA-Z0-9_\.]*|/)')

class String(Node):
    @classmethod
    def codify(cls, value):
        return '{0}{1}{0}'.format(cls.deliminator, value)

    @classmethod
    def escape(cls, value):
        return str(value).replace(cls.deliminator, cls.escaper)

    def __init__(self, string):
        self.string = string

    def evaluate(self, settings):
        def expand(match):
            lookup, = match.groups()
            if lookup == '/':
                return ''
            try:
                value = Reference(lookup.split('.')).get(settings.context)
            except ReferenceMissing:
                try:
                    value = settings.function(lookup)()
                except FallThrough as e:
                    value = e.result
                except ConversionError as e:
                    raise ReferenceMissing(lookup, settings.context)
            return self.escape(value)
        return lookup.sub(expand, self.string)

    def showhead(self):
        return '{2}: {0}{1}{0}'.format(self.deliminator, self.string, self.__class__.__name__)

    def subparse(self, parse):
        from naked import Naked
        result = parse(self.string + '\n')[0]
        indent, node = result.split()
        if not isinstance(node, Naked):
            node = Naked(node)
        node.push(self.deliminator)
        node.insert(self.deliminator)
        node.insert(indent)
        node.compress()
        return node


class String1(String):
    deliminator, counterpart, escaper = "'", '"', '"'


class String2(String):
    deliminator, counterpart, escaper = '"', "'", "'"


