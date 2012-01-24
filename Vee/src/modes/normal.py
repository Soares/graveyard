from .windows import api as w
from .base import Mode

class Normal(Mode):
	bindings = {
		4: lambda self: self.vee.quit(),
		261: lambda self: self.vee.modules['windows'].current.canvas.shift_cursor(1, 0),
		260: lambda self: self.vee.modules['windows'].current.canvas.shift_cursor(-1, 0),
		259: lambda self: self.vee.modules['windows'].current.canvas.shift_cursor(0, 1),
		258: lambda self: self.vee.modules['windows'].current.canvas.shift_cursor(0, -1),
		'h': lambda self: w.hsplit(self.vee.modules['windows'].current),
		'v': lambda self: w.vsplit(self.vee.modules['windows'].current),
		't': lambda self: w.tsplit(self.vee.modules['windows'].current),
		'c': lambda self: w.close(self.vee.modules['windows'].current),
		'l': lambda self: w.hnext(self.vee.modules['windows'].current),
		'r': lambda self: w.hprev(self.vee.modules['windows'].current),
		'j': lambda self: w.vnext(self.vee.modules['windows'].current),
		'k': lambda self: w.vprev(self.vee.modules['windows'].current),
		'n': lambda self: w.tnext(self.vee.modules['windows'].current),
		'p': lambda self: w.tprev(self.vee.modules['windows'].current),
	}
