"""
The Library:

A library is merely an object that holds a register of functions which can be
accessed from within cm files. Converter objects have a list of libraries,
which are used to find functions and filters while converting cm files.
To make your own, simply create an instance of Library and then register
functions using the library's register method.

When registering functions, you have a few options:

    name
        The name of the function as accessed from the cm file
        This defaults to the function name

    evaluate
        If True (which is the default), all arguments to the function will
        be evaluated before being passed to the function. This means that
        they will be strings.

        If False, all arguments to the function will still be Nodes in the AST.
        This means that you can set the values of variables in the context
        and modify the structure of the output file.
        Only use this if you know what you are doing.

        All filters must have evaluate = True

    receiving
        None, a string, or a list of strings
        In cm, functions can pass data to following functions. This feature
        allows 'if' and 'else' to be defined as simple functions, where 'if'
        passes data to 'else'. In order to determine whether or not a function
        takes the context data of the function before it, the 'receiving' list
        of the function is checked. If the tag of the extra data is in the
        receiving list, the extra data is passed to the function. Otherwise,
        it is not.

        For example, 'if' sends extra data under the 'if' tag. Both 'elif' and
        'else' have receiving lists of ['if']. Thus, they accept the extra
        data sent by the 'if' function, with the 'if' tag. They would not,
        however, except extra data from the 'for' function, which is sent with
        a 'for' tag.

        Note that in order for a function to be able to be called on its own,
        it must have 'None' in its receiver list. For example, 'else' will
        raise an exception if not called directly after 'if': 'else' can not
        be called on its own. If it's receiving list were [None, 'if'] then
        it could be called on its own, but this is not the desired behavior
        for else.

        The default receiving tag list is [None], which means that by default
        a function rejects any extra data but may be called without extra data.

        Because it is so common to only receive from one tag, you can give
        'receiving' as just a string. This will be interpreted as a list with
        a single tag. For example, registering 'else' with 'receiving="if"'
        is the same as registering it with 'receiving=["if"]'.

There are also a few decorators that alter the way that functions are called:
give_context and give_settings. See their documentation for details.

Registration gives certain attributes to the registered functions. If you are
putting lots of attributes on your functions, be warned that there may be some
collissions.
"""
from functools import partial

def give_context(fn):
    """
    Modifies a function so that, if it is registered with a library, the
    function will be given the current context as a keyword argument 'context'
    when called.
    """
    fn.give_context = True
    return fn

def give_settings(fn):
    """
    Modifies a function so that, if it is registered with a library, the
    function will be given the converter object as a keyword argument
    'settings' when called.
    Note that functions with evaluate=False will be given the converter
    object as a keyword argument no matter what, because they will need
    it to evaluate their arguments.
    """
    fn.give_settings = True
    return fn


class Library(object):
    def __init__(self, name=None):
        if name is None:
            import inspect
            frame = inspect.stack()[1]
            name = inspect.getmodule(frame[0]).__name__
        self.name = name
        self.functions = {}

    def get(self, name):
        return self.functions[name]

    def register(self, fn=None, name=None, evaluate=True, receiving=None):
        """
        Registers a function with the library.

        This can be used as a decorator. See the documentation for the module
        for information about how to use 'name', 'evaluate', and 'receiving'.

        If the first argument is a string instead of a function register
        curries itself with the string as the function name

        @register
        def fn(...) ...

        registers the function 'fn' with the name 'fn', while

        @register('fn2')
        def fn(...) ...

        registers the function 'fn' with the name 'fn2'

        register also curries if you omit the function argument, which
        allows for more flexible use as a decorator. For example,

        @register('else', receiving='if')
        def else_(...) ...

        Will register else_ under the name 'else', receiving tags ['if']
        """
        if fn is None:
            # @register(**kwargs)
            return partial(self.register, name=name,
                    evaluate=evaluate, receiving=receiving)
        if name is None and isinstance(fn, str):
            # @register(name, **kwargs)
            return self.register(name=fn,
                    evaluate=evaluate, receiving=receiving)
        elif isinstance(fn, str):
            name, fn = fn, name
        fn.evaluate = evaluate
        fn.receivers = receiving if receiving else [None]
        self.functions[name if name is not None else fn.__name__] = fn
        return fn

    def accepts(self, name, tag):
        """
        This function is used to determine whether or not a function in this
        library accepts additional information under the name 'tag'. It is
        through this feature that functions can pass information to following
        functions, such as 'if' passing information to 'else'

        Throws KeyError if the name isn't in the library
        """
        return tag in self.functions[name].receivers

    def __repr__(self):
        return self.name
