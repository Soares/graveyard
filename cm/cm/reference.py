"""
This object is used to gain references to objects in a context. References can
be used to get or set variables in a context. If a varible retrieved from a
context is callable, it will be called and the result will be retuned.
Otherwise, the variable itself will be returned.
Variables with an attribute named 'unsafe' will not be considered.

In cm, lookups are a list of names. For example, the lookup 'foo.bar.baz'
references the path ['foo', 'bar', 'baz'].

A reference gives you an option to get or set that path in a context. A
reference first tries to use indexing and then attempts to use attribute
access.

At each level of the path, the reference tries to get to the next level of the
path first through index lookup and then through attribute access.


>>> class Dict(dict): pass
...
>>> r = Reference(['foo'])
>>> c = Dict({'foo': 'index'})
>>> c.foo = 'attribute'
>>> r.get(c)
'index'

>>> c = Dict({})
>>> c.foo = 'attribute'
>>> r.get(c)
'attribute'


If there are multiple elements to the path then the lookup is recursive.
For example:


>>> c3 = Dict({'baz': 'result'})
>>> c2 = Dict({'bar': c3})
>>> c1 = Dict({'foo': c2})
>>> r = Reference('foo.bar.baz'.split('.'))
>>> r.get(c1)
'result'


You can also use references to set values in a context. It works like this:

Indexes are set first

>>> c = Dict({'foo': 'index'})
>>> c.foo = 'attribute'
>>> r = Reference(['foo'])
>>> r.set(c, 'set')
>>> c['foo']
'set'
>>> c.foo
'attribute'

Attributes are set if the name isn't present in the index and if the attribute
is present

>>> c = Dict()
>>> c.foo = 'attribute'
>>> r.set(c, 'set')
>>> 'foo' in c
False

Indexes are set if they aren't present and indexing is possible

>>> c = Dict()
>>> r.set(c, 'set')
>>> c['foo']
'set'

Attributes are set if indexing is not possible

>>> class Object(object): pass
...
>>> c = Object()
>>> r.set(c, 'set')
>>> c.foo
'set'
"""

class ReferenceMissing(Exception):
    def __init__(self, attribute, object):
        self.attribute, self.object = attribute, object
        super(ReferenceMissing, self).__init__()

    def __str__(self):
        from StringIO import StringIO
        f = StringIO()
        print >> f, self.attribute
        print >> f, '\tSearched in: %s' % self.object
        return f.getvalue()


class Reference(object):
    def __init__(self, path):
        self.path = path

    def get_with(self, getter, exception, object, attribute):
        try:
            value = getter(object, attribute)
            if not hasattr(value, 'unsafe'):
                return value() if callable(value) else value
        except exception:
            raise ReferenceMissing(attribute, object)
        
    def lookup(self, object, attribute):
        index = lambda o, a: o[a]
        ierror = (IndexError, TypeError, KeyError)
        try:
            return self.get_with(index, ierror, object, attribute)
        except ReferenceMissing:
            return self.get_with(getattr, AttributeError, object, attribute)

    def get(self, context):
        return reduce(self.lookup, self.path, context)

    def set(self, context, value):
        base, attr = reduce(self.lookup, self.path[:-1], context), self.path[-1]
        try:
            if attr in base:
                base[attr] = value
            elif hasattr(base, attr):
                setattr(base, attr, value)
            else:
                base[attr] = value
        except TypeError:
            setattr(base, attr, value)
