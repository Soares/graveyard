# coding: utf-8
from cm.nodes import Lookup
from helpers import twolist

def p_path(p):
    """path : path DOTNAME \n| DOTNAME"""
    p[0] = twolist(p, initial=1)


def p_lookup(p):
    """lookup : NAME path \n| NAME"""
    if len(p) is 2:
        p[0] = Lookup(p[1])
    else:
        p[0] = Lookup(p[1], *p[2])


def p_number(p):
    """number : FLOAT \n| INT"""
    p[0] = int(p[1]) if str(p[1]).isdigit() else float(p[1])


def p_expression(p):
    """
    expression : number
               | STRING
               | lookup
               | part
    """
    p[0] = p[1]
def p_expression_paren(p):
    """expression : '(' b expression b ')'"""
    p[0] = p[3]
