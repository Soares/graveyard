from helpers import twolist
from cm.nodes import Naked, Element, Line


def p_safemode(p):
    """safemode : '>' \n|"""
    p[0] = ''.join(p[1:])
def p_elemmode(p):
    """elemmode : '/' \n| safemode"""
    p[0] = ''.join(p[1:])


def p_classproperty(p):
    """classproperty : DOTNAME"""
    p[0] = 'class', p[1]
def p_idproperty(p):
    """idproperty : HASHNAME"""
    p[0] = 'id', p[1]
def p_nameproperty(p):
    """nameproperty : ATNAME"""
    p[0] = 'name', p[1]
def p_boolproperty(p):
    """boolproperty : COLINNAME"""
    p[0] = p[1], p[1]
def p_property(p):
    """property : classproperty \n| idproperty \n| nameproperty \n| boolproperty"""
    p[0] = p[1]
def p_properties(p):
    """properties : properties property \n|"""
    p[0] = twolist(p)


def p_tag(p):
    """tag : ELEMNAME properties maybe_parameters maybe_attributes"""
    p[0] = Element(p[1], p[2], p[3], p[4])
def p_div(p):
    """div : property properties maybe_parameters maybe_attributes"""
    p[2].insert(0, p[1])
    p[0] = Element('div', p[2], p[3], p[4])
def p_element(p):
    """element : tag \n| div"""
    p[0] = p[1]

def p_outelement(p):
    """outelement : element elemmode"""
    p[1].set_mode(p[2])
    p[0] = p[1]


def p_inelement(p):
    """inelement : element safemode brackets"""
    p[1].set_mode(p[2])
    if p[3] or p[1].consumes_body():
        p[1].set_body(p[3])
    p[0] = p[1]
def p_inelement2(p):
    """inelement : element '/' \n| element '/' '>'"""
    p[1].set_mode(''.join(p[2:]))
    p[0] = p[1]


def p_elemline(p):
    """elemline : outelement w linepart \n| inelement w linepart"""
    if p[1].consumes_body() and (p[2] or p[3]):
        p[1].oneline = True
        p[1].set_body(p[3])
        p[0] = p[1]
    elif not isinstance(p[3], Naked):
        p[1].oneline = True
        p[0] = Naked(p[1], p[2], p[3])
    elif not p[2] and not p[3]:
        p[0] = p[1]
    else:
        p[1].oneline = True
        p[3].insert(p[2])
        p[3].insert(p[1])
        p[0] = p[3]


def p_element_line(p):
    """element_line : indent elemline EOL"""
    p[0] = Line(p[1], p[2], lineno=p.lineno(3))
