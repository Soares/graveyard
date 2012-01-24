from node import Node
from cm.exceptions import ConversionError
from cm.reference import Reference

class Lookup(Node):
    def __init__(self, *path):
        self.path = list(path)
        self.reference = Reference(self.path)

    def normalize(self):
        if len(self.path) is not 1:
            raise ConversionError('You are attempting to use a non-normal '
                                  'lookup (%s) as a normal lookup.'
                                  % '.'.join(self.path))
        return self.path[0]

    def showhead(self):
        return 'Lookup %s' % '.'.join(self.path)

    def evaluate(self, settings):
        return settings.eval(self.reference.get(settings.context))
