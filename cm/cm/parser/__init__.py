from ply import yacc
from cm.nodes import EmptyLine
from cm.lexer import Lexer
tokens = Lexer.tokens

from whitespace import *
from expressions import *
from parameters import *
from functions import *
from sections import *
from elements import *
from naked import *

def p_emptyline(p):
    """empty_line : EOL"""
    p[0] = EmptyLine()

p_line = define("""
    line : element_line
         | section_line
         | function_line
         | empty_line
         | naked_line
""")


def p_statements(p):
    """statements : statements line \n|"""
    p[0] = twolist(p)


def p_error(p):
    raise SyntaxError('Syntax error: unexpected %s at line %d (%s)'
                       % (p.type, p.lineno, p.value))


p_file = define('file : statements')

def parser(debug=0, optimize=0):
    return yacc.yacc(start='file', debug=debug, optimize=optimize,
                     tabmodule='cm.parser.output.parsetab')
