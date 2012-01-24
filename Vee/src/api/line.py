def vline(string, x, y, length, attrs=None):
	import curses
	if length is 0:
		return
	for (index, char) in enumerate(string):
		char = ord(char) if isinstance(char, str) else char
		win = curses.newwin(length, 1, y, x + index)
		win.bkgd(char, attrs or 0)
		win.noutrefresh()


def hline(string, x, y, length, attrs=None):
	import curses
	if length is 0:
		return
	for (index, char) in enumerate(string):
		char = ord(char) if isinstance(char, str) else char
		win = curses.newwin(1, length, y + index, x)
		win.bkgd(char, attrs or 0)
		win.noutrefresh()


class Line:
	def __init__(self, x, y, width, fill='normal'):
		from .style import color
		self.x, self.y, self.width = x, y, width
		self.fill = color(fill) if isinstance(fill, str) else fill
		self.strings = []

	def add(self, string, attributes=None):
		if string:
			self.strings.append((string, attributes))

	def draw(self):
		from api import screen
		if not self.strings:
			return
		dx = 0
		for (string, attrs) in self.strings:
			screen.addstr(self.y, self.x + dx, string, attrs or 0)
			dx += len(string)
		if dx < self.width:
			screen.addstr(self.y, self.x + dx, ' ' * (self.width - dx), self.fill)
		screen.noutrefresh()
