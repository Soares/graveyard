from django import template
register = template.Library()


class FiletypeNode(template.Node):
    def __init__(self, type):
        self.type = template.Variable(type)
    def render(self, context):
        context.dicts[-1]['filetype'] = self.type.resolve(context)
        return ''

def do_filetype(parser, token):
    tokens = token.split_contents()
    if len(tokens) > 2:
        raise ValueError('%r tag takes at most one argument' % tokens[0])
    return FiletypeNode(tokens[1] if len(tokens) is 2 else 'html')

register.tag('filetype', do_filetype)


def filetype_tag(fn):
    class TagNode(template.Node):
        def __init__(self, *args):
            self.args = map(template.Variable, args)
        def render(self, context):
            return fn(*(v.resolve(context) for v in self.args), filetype=context['filetype'])
    def do_tag(parser, token):
        return TagNode(token.split_contents()[1:])
    register.tag(fn.__name__, do_tag)


@filetype_tag
def slash(filetype):
    return '/' if filetype == 'xhtml' else ''


@filetype_tag
def flag(name, filetype):
    return '{0}="{0}"'.format(name) if filetype == 'xhtml' else name
