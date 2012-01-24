"""
A builder parses a cm file into an AST.

It is a very stateful object, parsing more than one file per builder is not
reccomended, parsing more than one file with one builder on multiple threads
is not possible.

The build function of a builder takes a string (not a file or file-like object)
and parses it into an AST. Make sure you pass it a string, not a file.

>>> from cm.nodes import File
>>> b = Builder()
>>> isinstance(b.build('Hello, World!'), File)
True
"""
from cm.utilities.stream import Stream
from cm.parser import parser
from cm.nodes import File, EmptyLine
from cm.lexer import Lexer
from cm.exceptions import ConversionError, convert
import re

comment = re.compile(r'(\s*)(\\*)//.*(\n|\r|\n\r|\r\n)')
def subcomment(match):
    spaces, slashes, end = match.groups()
    if len(slashes) is 0:
        return end
    if len(slashes) % 2:
        return match.group(0)
    return spaces + slashes + end


class Builder(object):
    def __init__(self, debug=False, optimize=False):
        self.debug, self.optimize = debug, optimize
        self.parser = parser(debug=debug, optimize=optimize)

    def parse(self, input):
        lexer = Lexer().build(debug=self.debug, optimize=self.optimize,
                lextab='cm.lexer.output.lextab')
        try:
            return self.parser.parse(input, lexer=lexer, debug=self.debug)
        except SyntaxError as e:
            raise convert(e, self.context)

    def preparse(self, string):
        string = comment.sub(subcomment, string)
        return string + ('' if string.endswith('\n') else '\n')
        
    def build(self, string, context=None):
        self.indent = 0
        self.context = context
        self.stream = Stream(self.parse(self.preparse(string)))
        return File(*list(self.statements()))

    def statements(self):
        while True:
            line = self.stream.next()
            line.context = self.context
            if isinstance(line, EmptyLine):
                line.indentation = self.indent
            if line.indentation > self.indent:
                raise ConversionError('Unexpected indent at %s' % repr(line))
            elif line.indentation < self.indent:
                self.stream.backstep()
                raise StopIteration
            line.subparse(self)
            yield line

    def parse_body(self):
        self.indent += 1
        statements = list(self.statements())
        self.indent -= 1
        return statements
