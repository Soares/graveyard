import curses
from functools import reduce

colors = {}
fonts = {}
specials = {}

def initialize():
	curses.init_pair(1, -1, -1)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_CYAN)
	colors['normal'] = curses.color_pair(1)
	colors['disabled'] = curses.color_pair(2)
	colors['flashy'] = curses.color_pair(3)
	fonts['normal'] = curses.A_NORMAL
	fonts['underline'] = curses.A_UNDERLINE
	specials['|'] = curses.ACS_VLINE
	specials['-'] = curses.ACS_HLINE


def special(name):
	return specials[name]


def color(*names):
	return reduce(lambda flags, name: flags | colors[name], names, 0)


def font(*names):
	return reduce(lambda flags, name: flags | fonts[name], names, 0)
