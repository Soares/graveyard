from cm.nodes import Naked, Function, Line


def p_namedfn(p):
    """namedfn : FNNAME maybe_parameters maybe_attributes maybe_brackets"""
    p[0] = Function(p[1], p[2], p[3], p[4])
def p_unnamedfn(p):
    """unnamedfn : FNP varlist ')' maybe_attributes maybe_brackets"""
    p[0] = Function('', p[2], p[4], p[5])
def p_unnamedfn2(p):
    """unnamedfn : FNA attrlist '}' maybe_brackets"""
    p[0] = Function('', (), p[2], p[5])
def p_unnamedfn3(p):
    """unnamedfn : FNB inline ']'"""
    p[0] = Function('', (), (), p[2])
def p_function(p):
    """function : namedfn \n| unnamedfn"""
    p[0] = p[1]


def p_fnline(p):
    """fnline : function w linepart"""
    if not isinstance(p[3], Naked):
        p[0] = Naked(p[1], p[2], p[3])
    elif not p[2] and not p[3]:
        p[0] = p[1]
    else:
        p[3].insert(p[2])
        p[3].insert(p[1])
        p[0] = p[3]


def p_function_line(p):
    """function_line : indent fnline EOL"""
    p[0] = Line(p[1], p[2], lineno=p.lineno(3))
