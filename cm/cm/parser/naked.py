from helpers import define
from cm.nodes import Naked, Line

def p_noStartB(p):
    """
    noStartB : SPACES \n| TABS  \n| NIL \n| ESCAPEE \n| NAME \n| INT \n| FLOAT
             | STRING \n| OTHER \n| ',' \n| '('     \n| ')'  \n| '{' \n| '}'
             | '+'    \n| '-'   \n| '/' \n| '>'     \n| '='  \n| '[' \n| RAW
             | RAW4
    """
    p[0] = p[1]

p_part = define("""part : inelement \n| insection \n| function""")
p_linepart = define("""linepart : elemline \n| fnline \n| secline \n| naked""")
p_noStart = define("""noStart : noStartB \n| ']'""")

def p_inline(p):
    """inline : part inline \n| noStartB inline \n|"""
    if len(p) is 1:
        p[0] = Naked()
    elif isinstance(p[2], Naked):
        p[2].insert(p[1])
        p[0] = p[2]
    else:
        p[0] = Naked(p[1], p[2])

def p_naked(p):
    """naked : noStart linepart \n|"""
    if len(p) is 1:
        p[0] = Naked()
    elif isinstance(p[2], Naked):
        p[2].insert(p[1])
        p[0] = p[2]
    else:
        p[0] = Naked(p[1], p[2])

def p_naked_line(p):
    """naked_line : indent naked EOL"""
    p[0] = Line(p[1], p[2], lineno=p.lineno(3))
