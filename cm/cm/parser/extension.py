from cm.nodes import Extension

def p_names(p):
    """names : names w ',' w NAME \n| NAME"""
    if len(p) > 2:
        p[1].append(p[5])
    p[0] = [p[1]]


def p_extenison(p):
    """extension : '+' names EOL"""
    p[0] = Extension(*p[2])
