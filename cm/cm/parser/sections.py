from cm.nodes import Naked, Section, Line

def p_secmode(p):
    """secmode : '+' \n| '-' \n| '+' '-' \n| '-' '+' \n|"""
    p[0] = ''.join(p[1:])


def p_section(p):
    """section : SECNAME secmode"""
    p[0] = Section(p[1], p[2])


def p_insection(p):
    """insection : section brackets"""
    p[1].oneline = True
    p[1].set_body(p[2])
    p[0] = p[1]


def p_secline(p):
    """secline : insection w linepart"""
    if not isinstance(p[3], Naked):
        p[0] = Naked(p[1], p[2], p[3])
    elif not p[2] and not p[3]:
        p[0] = p[1]
    else:
        p[3].insert(p[2])
        p[3].insert(p[1])
        p[0] = p[3]


def p_section_line(p):
    """section_line : indent secline EOL \n| indent section EOL"""
    p[0] = Line(p[1], p[2], lineno=p.lineno(3))
