#!/usr/bin/python
def converter(debug=False, optimize=False):
    from cm import Converter, FileManager
    manager = FileManager('examples/input', 'examples/output')
    return Converter(manager, debug=debug, optimize=optimize)


def convert(filename, debug=False, optimize=False):
    return converter(debug, optimize).convert(filename)

def build(filename, debug=False, optimize=False):
    return converter(debug, optimize).build(filename)

def render(filename, debug=False, optimize=False):
    return converter(debug, optimize).render(filename)


def main():
    import sys
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-d', '--debug', action='store_true', dest='debug', help='convert in debugging mode')
    parser.add_option('-o', '--optimize', action='store_true', dest='optimize', help='convert in optimized mode')
    parser.add_option('-b', '--build', action='store_true', dest='build', help='only build the file, print the AST')
    parser.add_option('-r', '--render', action='store_true', dest='render', help='render and print the file')
    (options, args) = parser.parse_args(sys.argv[1:])
    filename = args[0] if len(args) else 'debug'
    if options.render:
        result = render(filename, options.debug, options.optimize)
    elif options.build:
        result = build(filename, options.debug, options.optimize)
    else:
        result = convert(filename, options.debug, options.optimize)
    print result
    return result


if __name__ == '__main__':
    main()
