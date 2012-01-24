from itertools import chain
from node import Body
from section import Section
from extension import is_extension, Extension
from cm.exceptions import ConversionError


class File(Body):
    def __init__(self, *statements):
        if len(statements) and is_extension(statements[0]):
            self.extension, self.statements = Extension(statements[0]), statements[1:]
        else:
            self.extension, self.statements = None, statements
        self.sectionmap = {}
        for section in self.sections():
            if section.name in self.sectionmap:
                raise ConversionError('Duplicate section: %s' % section.name)
            self.sectionmap[section.name] = section

    def children(self):
        return self.statements

    def showhead(self):
        if self.extension:
            return 'File extending %s' % self.extension
        return 'File'

    def sections(self):
        return chain(*(s.sections() for s in self.statements))

    def extend(self, file):
        for (name, section) in file.sectionmap.items():
            if name in self.sectionmap:
                self.sectionmap[name].become(section)

    def evaluate(self, settings):
        settings.context.push()
        getblock = lambda s: lambda: settings.eval(self.sectionmap[s])
        blocks = dict((s, getblock(s)) for s in self.sectionmap)
        settings.context['blocks'] = blocks
        exclude = (Section,) if self.extension else ()
        result = super(File, self).evaluate(settings, exclude=exclude)
        if self.extension:
            try:
                parent = settings.build(settings.eval(self.extension))
            except ConversionError as e:
                e.contexts.append(self.extension)
                raise
            parent.extend(self)
            return settings.eval(parent)
        settings.context.pop()
        return result
