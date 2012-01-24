import logging
import os

logging.logThreads = 0
logging.logProcesses = 0

root = logging.getLogger('vee')
root.setLevel(logging.DEBUG)

logdir = os.path.join(os.path.dirname(__file__), 'logs')
debug = logging.FileHandler(os.path.join(logdir, 'debug.log'), 'w')
debug.setLevel(logging.DEBUG)

info = logging.FileHandler(os.path.join(logdir, 'info.log'))
info.setLevel(logging.INFO)

error = logging.FileHandler(os.path.join(logdir, 'error.log'))
error.setLevel(logging.WARNING)

f_debug = logging.Formatter('%(levelname)s: %(message)s')
standard = logging.Formatter('%(levelname)s - %(name)s: %(message)s')

debug.setFormatter(f_debug)
info.setFormatter(standard)
error.setFormatter(standard)

root.addHandler(debug)
root.addHandler(info)
root.addHandler(error)

def handle_error(self, record):
	raise
logging.Handler.handleError = handle_error
