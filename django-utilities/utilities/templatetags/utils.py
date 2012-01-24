from django import template
from django.template import Node, Variable, Context, loader
from django.conf import settings
from django.utils.safestring import mark_safe
register = template.Library()

def taglist(tag):
    class TaglistNode(Node):
        def __init__(self, files, directory=None):
            self.directory = Variable(directory) if directory else None
            self.files = map(Variable, files)

        def render(self, context):
            directory = self.directory.resolve(context).rstrip('/') + '/' if self.directory else ''
            names = (directory + file.resolve(context) for file in self.files)
            return ''.join(tag % name for name in names)

    def do_taglist(parser, token):
        """
        {% tag file1 file2 file3 [in directory] %}
        You can use context variables as file names or directory names,
        so quote them if you don't want the name to be looked up as a variable
        """
        bits = token.split_contents()[1:]
        if len(bits) >= 2 and bits[-2] == 'in':
            return TaglistNode(bits[0:-2], bits[-1])
        return TaglistNode(bits)

    do_taglist.is_safe = True
    return do_taglist

style = taglist('<link rel="stylesheet" type="text/css" href="{media}css/%s.css">'.format(media=settings.MEDIA_URL))
register.tag('style', style)

script = taglist('<script type="text/javascript" src="{media}js/%s.js"></script>'.format(media=settings.MEDIA_URL))
register.tag('script', script)


class SectionNode(Node):
    def __init__(self, template, title, attrs, nodelist):
        self.template = template
        self.title = Variable(title)
        self.attrs = dict((name, Variable(val)) for (name, val) in attrs.iteritems())
        self.nodelist = nodelist

    def render(self, context):
        body = self.nodelist.render(context)
        title = self.title.resolve(context)
        attributes = dict((n, v.resolve(context)) for (n, v) in self.attrs.iteritems())
        attributes['class'] = attributes.get('class', '') + ' small section'
        attrs = mark_safe(' '.join('%s="%s"' % nv for nv in attributes.iteritems()))
        t = loader.get_template(self.template)
        return t.render(Context({
            'title': title, 'attrs': attrs, 'body': body,
        }))

def do_section(parser, token, template='parts/section.html', end='endsection'):
    """
    {% section "title" [attrname "attrvar"] %}
    ...
    {% endtop %}
    """
    bits = token.split_contents()[1:]
    if len(bits) is 0:
        title, attrs = '', {}
    elif len(bits) is 1:
        title, attrs = bits[0], {}
    elif len(bits) % 2 is 0:
        raise template.TemplateSyntaxError("Your attributes don't match up: %s" % ', '.join(bits[1:]))
    else:
        title = bits[0]
        attrs = dict(zip(bits[1::2], bits[2::2]))
    nodelist = parser.parse((end,))
    parser.delete_first_token()
    return SectionNode(template, title, attrs, nodelist)
do_section.is_safe = True

register.tag('section', do_section)


def around(range, index, amount=10):
    start = max(0, index-amount)
    end = index + amount
    return list(range)[start:end]

register.filter('around', around)


def safe_markdown(string):
    from markdown import markdown
    from django.utils.html import escape
    return mark_safe(markdown(escape(string)))

register.filter(safe_markdown)


@register.filter
def isin(item, list):
    return item in list


@register.filter
def datetime(date, format='%I:%m %p, %A %B %d, %Y'):
    return date.strftime(format)
