from ply.lex import TOKEN

def simply(str):
    return TOKEN(str)(lambda lexer, t: t)

def string(node):
    l = len(node.deliminator)
    @TOKEN(r'{0}[^{0}\n\t]*{0}'.format(node.deliminator))
    def token(lexer, t):
        t.type = 'STRING'
        t.value = node(t.value[l:-l])
        return t
    return token


def dropfirst(str):
    @TOKEN(str)
    def token(lexer, t):
        t.value = t.value[1:]
        return t
    return token


def unescaped(str):
    return r'(?<!\\)' + str


def name(str, restricted=True):
    body = r'[a-zA-Z][a-zA-Z0-9_-]*' if restricted else r'[a-zA-Z0-9_-]+'
    return dropfirst(unescaped(str + body))
