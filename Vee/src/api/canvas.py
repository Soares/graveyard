import curses
import exceptions

char = 2

class Canvas:
	def __init__(self, x, y, width, height):
		self.x, self.y, self.width, self.height = x, y, width, height
		self.window = curses.newwin(height, width, y, x)
		self.point = 0, 0
		from .style import color
		self.window.bkgd(' ', color('normal'))

		global char
		self.char = chr((char % 95) + 32)
		char += 1
		self.redraw()

	def __str__(self):
		return self.char

	def move(self, x, y):
		if x is not None: self.x = x
		if y is not None: self.y = y

	def resize(self, width, height):
		if width is not None: self.width = width
		if height is not None: self.height = height
		px, py = self.point
		self.point = min(px, self.width - 1), min(py, self.height - 1)
		# if self.point != (px, py): cursor.moved.send(to=self.point)

	def redraw(self):
		if self.width is 0 or self.height is 0:
			return
		y, x = self.window.getbegyx()
		h, w = self.window.getmaxyx()
		if h > self.height and w > self.width:
			self.window.resize(self.height, self.width)
		elif h > self.height:
			self.window.resize(self.height, w)
		elif w > self.width:
			self.window.resize(h, self.width)
		if y != self.y or x != self.x:
			self.window.mvwin(self.y, self.x)
		if h < self.height or w < self.width:
			self.window.resize(self.height, self.width)

		self.window.erase()
		#self.output(0, 0, self.char * (self.width * self.height - 1))
		self.window.noutrefresh()

	def output(self, x, y, string, style=None):
		self.window.addstr(y, x, string, style or 0)

	def take_cursor(self):
		self.set_cursor(*self.point)

	def set_cursor(self, x, y):
		if self.width is 0 or self.height is 0:
			return
		try:
			self.window.move(y, x)
		except curses.error:
			raise exceptions.OutOfBounds
		self.point = x, y
		self.window.noutrefresh()

	def shift_cursor(self, dx, dy):
		y, x = self.window.getyx()
		return self.set_cursor(dx + x, -dy + y)

	def close(self):
		del self.window
