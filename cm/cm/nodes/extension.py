from node import Node
from cm.exceptions import ConversionError
import re

extension = re.compile(r'^\+(\S*)$')

def is_extension(line):
    from cm.nodes import Naked, Function, Section
    node = line.node
    if not isinstance(node, Naked):
        return False
    if len(node.parts) is 1:
        return extension.match(node.parts[0])
    elif len(node.parts) is 2:
        return node.parts[0] == '+' and isinstance(node.parts[1], (Function, Section))
    return False

class Extension(Node):
    def __init__(self, node):
        self.naked = node

    def evaluate(self, settings):
        rendered = settings.eval(self.naked)
        self._render = rendered[1:]
        try:
            return extension.match(rendered).groups()[0]
        except AttributeError:
            raise ConversionError('Bad extension: %s' % rendered)

    def __repr__(self):
        return 'Extension "%s"' % getattr(self, '_render', 'unknown file')
