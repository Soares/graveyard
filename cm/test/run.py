#!/usr/bin/python
import unittest
import doctest
import cm
from cm import lexer, parser, nodes, converter
from cm.converter import (
    files,
    library,
    functions,
    reference,
    context, 
    builder,
    stream,
    utilities,
)

suite = unittest.TestSuite()
dtf = doctest.DocTestFinder(exclude_empty=False)
for mod in (cm, converter, files, library,
            functions, reference, context,
            builder, stream, utilities,
            lexer, parser, nodes):
    suite.addTest(doctest.DocTestSuite(mod, test_finder=dtf))
runner = unittest.TextTestRunner()
runner.run(suite)

import py.test
py.test.cmdline.main()
