from helpers import twolist

def p_attribute(p):
    """attribute : NAME b '=' b expression"""
    p[0] = (p[1], p[5])
def p_attribute2(p):
    """attribute : COLINNAME"""
    p[0] = (p[1], True)


def p_varlist(p):
    """varlist : expression c varlist \n|"""
    p[0] = [] if len(p) is 1 else [p[1]] + p[3]


def p_attrlist(p):
    """attrlist : attribute c attrlist \n|"""
    p[0] = twolist(p, new=1, list=3)


def p_parameters(p):
    """parameters : '(' b varlist ')'"""
    p[0] = p[3]
def p_maybe_parameters(p):
    """maybe_parameters : parameters \n|"""
    p[0] = p[1] if len(p) is 2 else []


def p_attributes(p):
    """attributes : '{' b attrlist '}'"""
    p[0] = p[3]
def p_maybe_attributes(p):
    """maybe_attributes : attributes \n|"""
    p[0] = p[1] if len(p) is 2 else []


def p_brackets(p):
    """brackets : '[' inline ']'"""
    p[0] = p[2]
def p_maybe_brackets(p):
    """maybe_brackets : brackets \n|"""
    p[0] = p[1] if len(p) is 2 else None
