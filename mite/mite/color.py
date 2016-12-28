"""Mite terminal coloring."""
import subprocess

# Grab the colors from the system.
try:
	BOLD = subprocess.check_output(['tput', 'bold'])
	RED = subprocess.check_output(['tput', 'setaf', '1'])
	GREEN = subprocess.check_output(['tput', 'setaf', '2'])
	YELLOW = subprocess.check_output(['tput', 'setaf', '3'])
	BLUE = subprocess.check_output(['tput', 'setaf', '4'])
	VIOLET = subprocess.check_output(['tput', 'setaf', '5'])
	TEAL = subprocess.check_output(['tput', 'setaf', '6'])
	WHITE = subprocess.check_output(['tput', 'setaf', '7'])
	BLACK = subprocess.check_output(['tput', 'setaf', '8'])
	RESET = subprocess.check_output(['tput', 'sgr0'])
except subprocess.CalledProcessError:
	COLORED = False
else:
	COLORED = True


def color(text, *escapes):
	if COLORED:
		esc = (b''.join(escapes)).decode('utf-8')
		return esc + text + RESET.decode('utf-8')
	return text
