"""
A context is a StackDict used to hold the current context of a cm file. See
the reference on StackDict for API details.
"""
from cm.utilities import StackDict

class Unsafer(type):
    def __init__(cls, *args, **kwargs):
        super(Unsafer, cls).__init__(*args, **kwargs)
        def override(name):
            def new(self, *args, **kwargs):
                return getattr(super(cls, self), name)(*args, **kwargs)
            override.unsafe = True
            setattr(cls, name, new)
        for name in ('pop', 'push', 'previous', 'update',
                     'has_key', 'get', 'setdefault'):
            override(name)


class Context(StackDict):
    __metaclass__ = Unsafer

    def __init__(self, *args, **kwargs):
        super(Context, self).__init__(*args, **kwargs)
        self.globals = {}
