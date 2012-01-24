import sys
import subprocess

not_configured = """CM is not configured to handle SASS conversion.
To enable SASS conversion, CM needs to have access to a sass executable that it
can use to convert SASS data to CSS. There are two ways that you can point CM
towards your SASS executable:

    1. You can configure CM with the --sass parameter as an absolute path to
    the sass executable. Before installing CM, just run:

    python setup.py config --sass=/path/to/sass/executable

    and then run 'python setup.py install', and your CM will work with SASS.


    2. Alternatively, configure your converter with the 'sass' parameter when
    you use CM. If you are using the CM API, this just involves putting

    'sass': '/path/to/sass/executable'

    in the configuration dictionary of the Converter object. See documentation
    on cm.Converter for details on configuring the converter.
    
    From the command line, this involves running cm with the --sass option,
    similar to above:

    cm infile outfile --sass=/path/to/sass/executable

    See documentation on the 'cm' executable for details on configuring cm
    from the command line.
"""

def sass(data, sasser, stderr=sys.stderr, compression='nested'):
    if sasser is None:
        raise ValueError(not_configured)
    call = (sasser, '-s', '-t', compression)
    proc = subprocess.Popen(call, stderr=stderr,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return proc.communicate(data)[0]
