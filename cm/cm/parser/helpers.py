def PARSER(string):
    def decorate(fn):
        fn.__doc__ = string
        return fn
    return decorate

def define(string, set=True, default=None):
    @PARSER(string)
    def parser(p):
        if set and len(p) > 1:
            p[0] = p[1]
        else:
            p[0] = default
    return parser

def twolist(p, length=None, list=1, new=2, initial=None):
    length = length or max(list, new) + 1
    if len(p) is length:
        p[list].append(p[new])
        return p[list]
    return [] if initial is None else [p[initial]]
