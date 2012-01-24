from cm.library import Library
library = Library()


def pairs(list):
    for i in range(len(list) - 1):
        yield (list[i], list[i+1])


@library.register
def add(*args):
    try:
        return reduce(lambda x, y: x + y, args)
    except TypeError:
        return reduce(str.__add__, map(str, args), '')

operation = lambda op: lambda *args: reduce(op, args)
chain = lambda op: lambda *args: all(op(x, y) for (x, y) in pairs(args))

library.register('sub', operation(lambda x, y: x - y))
library.register('mul', operation(lambda x, y: x * y))
library.register('div', operation(lambda x, y: x / y))
library.register('mod', operation(lambda x, y: x % y))

library.register('eq', chain(lambda x, y: x == y))
library.register('gt', chain(lambda x, y: x > y))
library.register('lt', chain(lambda x, y: x < y))
library.register('neq', chain(lambda x, y: x != y))
library.register('gte', chain(lambda x, y: x >= y))
library.register('lte', chain(lambda x, y: x <= y))

library.register('not', lambda x: not(x))
library.register('and', lambda *args: all(args))
library.register('or', lambda *args: any(args))
