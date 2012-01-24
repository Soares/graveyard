# coding: utf-8
from helpers import simply, string, unescaped, name
from ply.lex import lex, TOKEN
from cm.nodes import String1, String2

def strip_indents(body):
    lines = body.split('\n')
    if len(lines) is 1 or lines[0] != '':
        return body
    left = len(lines[1]) - len(lines[1].lstrip())
    return '\n'.join(line[left:] for line in lines)


class Lexer(object):
    tokens = (
        'RAW4', 'RAW', 'SPACES', 'TABS', 'NIL', 'ESCAPEE',

        'FNNAME', 'FNP', 'FNA', 'FNB',
        'SECNAME', 'ELEMNAME',
        'DOTNAME', 'COLINNAME', 'HASHNAME', 'ATNAME',
        'NAME', 'INT', 'FLOAT', 'STRING',

        'EOL', 'OTHER',
    )
    literals = ',(){}[]+-/>='
    escapees = (
        r'\\', r'\[', r'\]', r'\{', r'\}', r'\(', r'\)',
        r'\%', r'\*', r'-', r'\.', r':', r'\#', r'@',
        r'\+', r'/', r'>',
    )

    t_SPACES = r'\ +'
    t_TABS = r'\t+'

    t_FNNAME = name(r'%')
    t_FNP = unescaped(r'%\(')
    t_FNA = unescaped(r'%\{')
    t_FNB = unescaped(r'%\[')
    t_SECNAME = name(r'\*')
    t_ELEMNAME = name(r'-', False)
    t_DOTNAME = name(r'\.', False)
    t_COLINNAME = name(r':', False)
    t_HASHNAME = name(r'\#', False)
    t_ATNAME = name(r'@', False)
    t_NAME = simply('[a-zA-Z][a-zA-Z0-9_-]*')
    t_INT = simply(r'\d+')
    t_FLOAT = simply(r'\d*\.\d+')
    t_STRING1 = string(String1)
    t_STRING2 = string(String2)
    def t_RAW4(lexer, t):
        r'(?<!\\)\*\*\*\*(.|[\n\r])*?(?<!\\)\*\*\*\*'
        t.lexer.lineno += t.value.count('\n')
        t.value = t.value[4:-4]
        return t
    def t_RAW(lexer, t):
        r'(?<!\\)\*\*\*(.|[\n\r])*?(?<!\\)\*\*\*'
        t.lexer.lineno += t.value.count('\n')
        t.value = strip_indents(t.value[3:-3])
        return t
    def t_NIL(lexer, t):
        r'\\v'
        t.value = ''
        return t
    @TOKEN('({0})'.format('|'.join(map(r'\\{0}'.format, escapees))))
    def t_ESCAPEE(self, t):
        t.value = t.value[1:]
        return t
    def t_EOL(self, t):
        r'[\n\r]'
        t.lexer.lineno += 1
        return t
    def t_error(self, t):
        t.type = 'OTHER'
        t.value = t.value[0]
        t.lexer.skip(1)
        return t

    def build(self, **kwargs):
        return lex(module=self, **kwargs)
