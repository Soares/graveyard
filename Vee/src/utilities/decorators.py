from functools import update_wrapper, partial, reduce

def with_fn(decorator):
    """
    Allows a decorator to take mode arguments.
    The first argument is the function to decorate, which defaults to None.
    If the decorator is called without the function, it partially evaluates
    itself with the keyword arguments and waits for the function to decorate.
    Check it out:

    >>> @with_fn
    ... def test(fn, name='Just'):
    ...     return name
    ...
    >>> @test
    ... def a(): return
    ...
    >>> @test(name='another')
    ... def b(): return
    ...
    >>> @test(name='python hacker')
    ... def c(): return
    ...
    >>> ' '.join((a, b, c))
    'Just another python hacker'
    """
    def real_decorator(fn=None, *args, **kwargs):
        if fn is None:
            return partial(real_decorator, *args, **kwargs)
        return decorator(fn, *args, **kwargs)
    update_wrapper(real_decorator, decorator)
    return real_decorator


@with_fn
def decorator(doubledec=None, after=()):
    """
    Turns a function of (fn, *args, **kwargs) into a decorator that
    decorates function, waits for *args and **kwargs, and then applies
    the decorator.

    Use this when you have a decorator that does no preparation but merely
    creates an inner funtion and immediately returns it.

    @after is a list of decorators that allows you to preform modifications on
    the decorated function once instead of each time it is called, which would
    otherwise be impossible.

    >>> @decorator
    ... def add_one_to_first_arg(fn, a):
    ...     return fn(a+1)
    ...
    >>> @add_one_to_first_arg
    ... def addone(x):
    ...     return x
    ...
    >>> addone(2)
    3

    And here's how the after thing works:

    >>> @decorator(after=[add_one_to_first_arg])
    ... def add_two_to_first_arg(fn, a):
    ...     return fn(a+1)
    ...
    >>> @add_two_to_first_arg
    ... def addtwo(x):
    ...     return x
    ...
    >>> addtwo(2)
    4
    """
    def real_decorator(fn):
        fn = reduce(lambda fn, dec: dec(fn), after, fn)
        return lambda *args, **kwargs: doubledec(fn, *args, **kwargs)
    update_wrapper(real_decorator, doubledec)
    return real_decorator


def class_decorator(decorator):
	return lambda *args, **kwargs: lambda cls: decorator(cls, *args, **kwargs)


def monkey_patch(model, *decorators):
    return lambda fn: setattr(model, fn.__name__, reduce(lambda f, d: d(f), decorators, fn))
