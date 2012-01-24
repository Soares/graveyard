from structures import StackDict, ListDict

def indent(string, tab='\t'):
    return '\n'.join(tab + line for line in string.split('\n'))
