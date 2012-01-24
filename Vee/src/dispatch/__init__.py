"""Multi-consumer multi-producer dispatching mechanism

Originally based on django.dispatch (BSD) which was originally based on pydispatch
(BSD) http://pypi.python.org/pypi/PyDispatcher/2.0.1.
See license.txt for original licenses.

Modified for Vee's purposes.
"""

from .dispatcher import Signal
