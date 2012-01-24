import exceptions

class Mode:
	bindings = {}

	def __init__(self, vee):
		self.vee = vee

	def dispatch(self, char):
		try:
			if char in self.bindings:
				self.bindings[char](self)
			elif char in range(256) and chr(char) in self.bindings:
				self.bindings[chr(char)](self)
		except (exceptions.OutOfBounds, exceptions.NotEnoughSpace):
			pass
