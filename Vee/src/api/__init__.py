import curses

screen = None


class Root:
	def run(self):
		import locale
		locale.setlocale(locale.LC_ALL, '')
		curses.wrapper(self.initialize)

	def x(self):
		return self.root.getbegyx()[1]

	def y(self):
		return self.root.getbegyx()[0]

	def width(self):
		return self.root.getmaxyx()[1] - self.x()

	def height(self):
		return self.root.getmaxyx()[0] - self.y()

	def initialize(self, scrn):
		global screen
		screen = scrn

		from . import style
		curses.raw()
		curses.use_default_colors()
		style.initialize()
		self.root = screen
		self.root.bkgd(' ', style.color('disabled'))
		self.root.noutrefresh()

		self.setup()

		self.exit = False
		self.mainloop()

	def setup(self):
		pass

	def mainloop(self):
		while not self.exit:
			self.update()
			self.dispatch(self.root.getch())

	def refresh(self):
		self.root.noutrefresh()
	
	def update(self):
		curses.doupdate()

	def dispatch(self, char):
		raise NotImplementedError

	def quit(self):
		self.exit = True
