from cm.functions import FallThrough
from cm.reference import ReferenceMissing
from cm.utilities import indent

class ConversionError(Exception):
    """Raised only when a specific conversion error can be identified"""
    def __init__(self, *args, **kwargs):
        self.contexts = list(kwargs.pop('contexts', []))
        self.original = kwargs.pop('original', None)
        super(ConversionError, self).__init__(*args, **kwargs)

    def __str__(self):
        from StringIO import StringIO
        f = StringIO()
        print >> f, ''
        if self.original:
            print >> f, self.original
        else:
            print >> f, ''
        for item in reversed(self.contexts):
            print >> f, 'In %s:' % `item`
        for arg in self.args:
            print >> f, indent(arg).rstrip()
        return f.getvalue()


def convert(exception, *contexts):
    from StringIO import StringIO
    import traceback
    import sys
    f = StringIO()
    etype, evalue, tb = sys.exc_info()
    e = traceback.format_exception_only(etype, evalue)[-1]
    t = ''.join(traceback.format_tb(tb))
    raise ConversionError(e, original=t, contexts=contexts)
