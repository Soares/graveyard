"""
The File Manager:

This object is used to load .cm files for conversion.  The file manager doesn't
actually touch anything to do with cm, it just loads files.

The File Manager is used by the Conveter object, and you can write your own.
The only required methods are input_file and output_file, the former which
should load a cm file for reading and the latter which should open an output
file for writing.

The default file manager can be given an input directory an an output
to use to load its files.

If you attempt to find a file with no extension, the default file manager will
check the same file name with a '.cm' extension if the extensionless-file does
not exist.

Similarly, if you load an output file with no extension or with a .cm
extension, the file manager will set the extension to '.html'.

If you don't like this behavior, it is fairly easy to write your own file
manager which you can give to your Converter.
"""
import os
from exceptions import ConversionError

class FileNotFound(ConversionError):
    pass


def file_exists(filename):
    if not os.path.exists(filename):
        return False
    try:
        os.listdir(filename)
    except OSError:
        return True
    return False


class FileManager(object):
    input_extension = '.cm'
    output_extension = '.html'

    def __init__(self, directory='', outdir=''):
        self.directory, self.outdir = directory.rstrip('/'), outdir.rstrip('/')

    def input_file(self, filename):
        if self.directory:
            full = os.path.join(self.directory, filename)
        inx = self.input_extension
        if file_exists(full):
            return open(full, 'r')
        elif not filename.endswith(inx) and file_exists(full + inx):
            try:
                return open(full + inx, 'r')
            except IOError:
                raise FileNotFound(filename)
        base, last = os.path.split(filename)
        if last.startswith('_'):
            raise FileNotFound(filename)
        return self.input_file(os.path.join(base, '_' + last))

    def output_file(self, filename):
        outx, inx = self.output_extension, self.input_extension
        if filename.endswith(inx):
            filename = filename[:-len(inx)]
        if not filename.endswith(outx) or not filename.count('.'):
            filename += outx
        if self.outdir:
            filename = os.path.join(self.outdir, filename)
        return open(filename, 'w')

    def relname(self, file):
        return file.name.split(self.directory)[-1].lstrip('/')
