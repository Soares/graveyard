from exceptions import ConversionError
from files import FileManager
from builder import Builder
from context import Context
from nodes import Node
from functions import calculator, html, FallThrough
import functions
import elements

class Converter(object):
    libraries = [calculator.library, functions.library, html.library]
    elemlibraries = [elements.library]
    filetype = 'html'

    def __init__(self, manager=FileManager, context={}, config={},
                 compress=False, debug=False, optimize=False):
        self.context = Context(true=True, false=False)
        self.context.update(context)
        self.config = config
        self.manager = manager() if callable(manager) else manager
        self.compress = compress
        self.builder = Builder(debug, optimize)

    def eval(self, element):
        if element is None:
            return ''
        if not isinstance(element, Node):
            return element
        try:
            return element.evaluate(self)
        except FallThrough as e:
            return e.result

    def accepts(self, name, tag):
        function = self.function(name)
        return tag in self.function(name).receivers

    def function(self, name):
        for library in reversed(self.libraries):
            try:
                return library.get(name)
            except KeyError:
                continue
        raise ConversionError('Could not find function %s' % name,
                'Libraries searched: %s' % list(reversed(self.libraries)))

    def element(self, name):
        for library in reversed(self.elemlibraries):
            try:
                return library.get(name)
            except KeyError:
                continue
        return elements.Element

    def configuration(self, name):
        if name in self.config:
            return self.config
        import cm.config
        return getattr(cm.config, name, None)

    def join(self, lines, compress=False):
        if compress or self.compress:
            return ''.join(str(line).strip() for line in lines)
        return '\n'.join(map(str, lines))

    def build(self, filename):
        file = self.manager.input_file(filename)
        name = self.manager.relname(file)
        return self.builder.build(file.read(), name)

    def render(self, filename, context=None):
        self.context.update(context or {})
        result = self.eval(self.build(filename))
        self.context.pop()
        return result

    def convert(self, filename, outname=None, context=None):
        file = self.manager.output_file(outname or filename)
        file.write(self.render(filename, context))
        return file.name
